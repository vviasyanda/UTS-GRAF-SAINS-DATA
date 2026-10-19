import os
import sys
import argparse
import pandas as pd
from tqdm import tqdm
from neo4j import GraphDatabase


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Impor dataset RetailRocket ke Neo4j."
    )
    parser.add_argument("-u", "--user", default="neo4j")
    parser.add_argument("-p", "--password", required=True)
    parser.add_argument("-b", "--bolt", default="neo4j://127.0.0.1:7687")
    parser.add_argument("-s", "--source", default="data")
    parser.add_argument("-d", "--database", default="neo4j")
    parser.add_argument("--batch-size", type=int, default=1000)
    return parser.parse_args()


def create_constraints(session):
    session.run("""
        CREATE CONSTRAINT visitor_id_unique IF NOT EXISTS
        FOR (v:Visitor)
        REQUIRE v.visitorId IS UNIQUE
    """).consume()

    session.run("""
        CREATE CONSTRAINT item_id_unique IF NOT EXISTS
        FOR (i:Item)
        REQUIRE i.itemId IS UNIQUE
    """).consume()


def import_batch(tx, batch):
    query = """
    UNWIND $batch AS row
    MERGE (v:Visitor {visitorId: row.visitorid})
    MERGE (i:Item {itemId: row.itemid})
    WITH v, i, row

    CALL (v, i, row) {
        WITH v, i, row
        WHERE row.event = 'view'
        CREATE (v)-[:VIEWED {
            timestamp: row.timestamp
        }]->(i)

        UNION ALL

        WITH v, i, row
        WHERE row.event = 'addtocart'
        CREATE (v)-[:ADDED_TO_CART {
            timestamp: row.timestamp
        }]->(i)

        UNION ALL

        WITH v, i, row
        WHERE row.event = 'transaction'
        CREATE (v)-[:BOUGHT {
            timestamp: row.timestamp,
            transactionId: row.transactionid
        }]->(i)
    }
    """

    tx.run(query, batch=batch).consume()


def main():
    args = parse_arguments()
    csv_file_path = os.path.join(args.source, "events.csv")

    if not os.path.exists(csv_file_path):
        print(f"File tidak ditemukan: {csv_file_path}")
        sys.exit(1)

    if args.batch_size <= 0:
        print("Batch size harus lebih besar dari 0.")
        sys.exit(1)

    try:
        driver = GraphDatabase.driver(
            args.bolt,
            auth=(args.user, args.password)
        )
        driver.verify_connectivity()
    except Exception as e:
        print(f"Gagal terhubung ke Neo4j: {e}")
        sys.exit(1)

    try:
        with driver.session(database=args.database) as session:
            create_constraints(session)

            chunks = pd.read_csv(
                csv_file_path,
                chunksize=args.batch_size,
                dtype={
                    "visitorid": "int64",
                    "itemid": "int64",
                    "event": "string",
                    "transactionid": "string"
                }
            )

            print("Memulai impor data RetailRocket...")

            for chunk in tqdm(chunks, desc="Mengimpor Batch Data"):
                chunk["transactionid"] = (
                    chunk["transactionid"].fillna("")
                )

                records = chunk.to_dict(orient="records")
                session.execute_write(import_batch, records)

            print("Proses impor berhasil.")

    finally:
        driver.close()


if __name__ == "__main__":
    main()
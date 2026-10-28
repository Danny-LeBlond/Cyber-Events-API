
from src.api import app, db
from api import models  
from api.models import CyberEvent
import csv
from datetime import datetime
with app.app_context():
    print("Models bound to metadata:", db.Model.metadata.tables.keys())
    db.drop_all()
    db.create_all()
    print("Tables created:", list(db.metadata.tables.keys()))
    count = 0
    with open('data/cyber_events.csv', newline='', encoding='latin-1') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                event = CyberEvent(
                    id=row['slug'],
                    date=datetime.strptime(row['event_date'], '%Y-%m-%d').date() if row['event_date'] else None,
                    year=int(row['year']) if row['year'] else None,
                    month=int(row['month']) if row['month'] else None,
                    actor=row['actor'][:75],
                    motive=row['motive'][:75],
                    victim=row['organization'][:100],
                    records_lost=int(row['industry_code']) if row['industry_code'] else None,
                    sector=row['industry'][:100],
                    type_of_incident=row['event_type'][:75],
                    action=row['event_subtype'][:75],
                    action_detail='',  # Not in CSV
                    summary=row['description'][:300],
                    source_link=row['source_url'][:200],
                    country=row['country'][:100],
                    state=row['actor_country'][:100]
                )
                db.session.add(event)
                count += 1
                if count % 100 == 0:
                    print(f"{count} rows inserted...")
            except Exception as e:
                print(f"Error adding row: {row.get('slug', '[no id]')} - {e}")
    db.session.commit()
    print(" Cyber events data inserted")

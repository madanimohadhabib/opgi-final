from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL("""
            CREATE TRIGGER mytable_insert_trigger
            ON mytable
            AFTER INSERT
            AS
            BEGIN
              PRINT 'A row has been inserted into mytable.'
            END
        """),
    ]

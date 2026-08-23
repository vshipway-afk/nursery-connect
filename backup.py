import shutil
import os
from datetime import datetime

# 1. Define where the database is and where backups should go
source_db = "nursery.db"
backup_folder = "database_backups"

# 2. Create the backup folder if it doesn't exist yet
if not os.path.exists(backup_folder):
    os.makedirs(backup_folder)

# 3. Create a unique name for the backup using the current date and time
# Example: nursery_backup_2026-08-23_19-30-00.db
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
backup_filename = f"nursery_backup_{timestamp}.db"
backup_path = os.path.join(backup_folder, backup_filename)

# 4. Copy the database safely
try:
    shutil.copy2(source_db, backup_path)
    print(f"✅ SUCCESS: Database safely backed up to -> {backup_path}")
except FileNotFoundError:
    print("❌ ERROR: Could not find 'nursery.db'. Make sure the database exists!")
except Exception as e:
    print(f"❌ ERROR: Something went wrong: {e}")
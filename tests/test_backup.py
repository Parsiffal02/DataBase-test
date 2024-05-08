import pytest
import os
import subprocess

# Абсолютные пути к утилитам pg_dump и psql
pg_dump_path = "C:\\Program Files\\PostgreSQL\\16\\bin\\pg_dump.exe"
psql_path = "C:\\Program Files\\PostgreSQL\\16\\bin\\psql.exe"

# Директория для хранения бэкапа
backup_dir = "C:\\Users\\ndedov\\Desktop"

# Пароль для доступа к базе данных
password = "1122"

@pytest.fixture(scope="module")
def backup_and_restore():
    # Создание бэкапа
    backup_file = create_backup(pg_dump_path, backup_dir, password)
    assert backup_file is not None, "Ошибка создания бэкапа."

    # Восстановление данных из бэкапа
    restore_success = restore_backup_data(psql_path, backup_file, password)
    assert restore_success, "Ошибка восстановления данных из бэкапа."

    yield

    # Удаление файла бэкапа после завершения теста
    if os.path.exists(backup_file):
        os.remove(backup_file)

def create_backup(pg_dump_path, backup_dir, password):
    backup_file = os.path.join(backup_dir, "backup.sql")
    command = f'"{pg_dump_path}" -U postgres -d resto -W {password} -f "{backup_file}"'
    try:
        subprocess.run(command, shell=True, check=True, timeout=60)
        return backup_file
    except subprocess.TimeoutExpired:
        print("Ошибка при создании бэкапа: Превышено время ожидания.")
        return None
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при создании бэкапа: {e}")
        return None

def restore_backup_data(psql_path, backup_file, password):
    command = f'"{psql_path}" -U postgres -d resto -W {password} -f "{backup_file}"'
    try:
        subprocess.run(command, shell=True, check=True, timeout=60)
        return True
    except subprocess.TimeoutExpired:
        print("Ошибка при восстановлении данных: Превышено время ожидания.")
        return False
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при восстановлении данных: {e}")
        return False

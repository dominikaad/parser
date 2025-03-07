from loader import cursor, bot, scheduler, con
from script.parser import parser_update

def update_bot():
    cursor.execute("SELECT * FROM users")
    a = cursor.fetchall()
    for i in a:
        id_user = i[0]
        task = scheduler.add_job(parser_update,
                                 trigger='interval',
                                 seconds=1,
                                 kwargs={'user_id': id_user, 'bot': bot})
        id_task = task.id
        cursor.execute(
            "UPDATE users SET id_task = (?) WHERE id = (?)",
        [id_task, id_user])
        con.commit()
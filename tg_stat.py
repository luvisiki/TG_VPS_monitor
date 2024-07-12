import os
import json
import asyncio
from datetime import datetime
from tg_bot import Bot

async def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    settings_path = os.path.join(script_dir, 'settings.json')
    stat_id_path = os.path.join(script_dir, 'tg_stat_id.txt')
    vnstat_m_path = os.path.join(script_dir, 'vnstat_m.png')
    vnstat_s_path = os.path.join(script_dir, 'vnstat_s.png')

    with open(settings_path, 'r') as f:
        settings = json.loads(f.read())
        servername = settings['servername']
        total_traff = settings['total_traff_stat']
        traff_methd = settings['traff_methd_stat']
        ifce = settings['ifce_stat']

    bot = Bot()

    try:  # 以防文件不存在炸了
        with open(stat_id_path, 'r') as ids:
            for id in ids:
                id = int(id.strip())
                await bot.delete_msg(id)
    except FileNotFoundError:
        pass

    os.system(f'vnstati -i {ifce} -m -o {vnstat_m_path}')
    os.system(f'vnstati -i {ifce} -s -o {vnstat_s_path}')

    nowdate = f"{datetime.now().year}年{datetime.now().month}月{datetime.now().day}日"
    hello = f"{servername}\n节点总流量{total_traff}({traff_methd})\n今天是{nowdate}\n以下是当前流量统计信息："

    with open(stat_id_path, 'w') as id_file:
        res = await bot.send_text(hello)
        if res:
            id_file.write(f"{res.message_id}\n")
        res = await bot.send_image(vnstat_s_path)
        if res:
            id_file.write(f"{res.message_id}\n")
        res = await bot.send_image(vnstat_m_path)
        if res:
            id_file.write(f"{res.message_id}\n")

    os.remove(vnstat_m_path)
    os.remove(vnstat_s_path)

if __name__ == "__main__":
    asyncio.run(main())

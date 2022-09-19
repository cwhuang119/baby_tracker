

import datetime

def format_query_all_content(query_content,baby):
    header = {
        "Daiper":"尿布",
        "Feed":"進食",
        "Weight":"體重",
        "Temperature":"體溫",
        "Height":"身高",
        "HeadLength":"頭圍"
    }
    result = f"寶寶:{baby.name}\n\n"
    dates = {}
    for query_type,db_rows in query_content.items():
        if len(db_rows)>0:
            section_result = f"{header[query_type]}:\n"
            dates[query_type]=[]
            for db_row in db_rows:
                time_format = '%Y/%m/%d'
                log_date = datetime.datetime.fromtimestamp(db_row.time_stamp).strftime(time_format)
                if log_date not in dates[query_type]:
                    dates[query_type].append(log_date)
                    section_result+=f"\n{log_date}\n"
                section_result+=db_row.format_log_str()
            section_result+='\n'
            result+=section_result
    return result


def format_log_str(db_row):
    return db_row.format_log_str()

def gen_line_ask_time():
    return "請輸入日期與時間ex:202208081717"

def gen_line_log_failed():
    return "登記失敗，請重新操作！"

def gen_lines_Log(baby,sitter,request_type,request_data,follow_up):

    follow_up_lines = {
        "Feed":"請輸入奶量(ml)",
        "Weight":"請輸入體重(g)",
        "Temperature":"請輸入體溫(c)",
        "Height":"請輸入身高(cm)",
        "HeadLength":"請輸入頭圍(cm)"
    }

    success_lines = {
        "Feed":["喝奶","ml"],
        "Weight":["體重","g"],
        "Temperature":["體溫","度"],
        "Height":["身高","cm"],
        "HeadLength":["頭圍","cm"],
    }

    # gen follow up lines
    if follow_up:
        return follow_up_lines[request_type]
    #gen success lines
    else:
        baby_name = baby.name
        sitter_name = sitter.name
        msg = f"{sitter_name}紀錄{baby_name}"
        if request_type=='Daiper':
            if request_data=='1':
                change_type = '小便'
            else:
                change_type = '大便'
            msg+=f"{change_type}一次"
        else:
            msg+=f"{success_lines[request_type][0]}{request_data}{success_lines[request_type][1]}"
        return msg



import datetime


def FormatDate(date, format_date):
    """
    converts the date to a convenient format
    :param datetime.datetime date:
    :param str format_date:
    :return: Returns the str object with the date.
    """
    date, time = str(date).split()
    year, month, day = date.split("-")
    hour, minute, second = time.split(":")
    result = format_date
    for i in range(len(format_date)):
        if format_date[i] == "%" and i != len(format_date)-1:
            if format_date[i+1] == "Y":
                result = result.replace("%Y", str(year))
            elif format_date[i+1] == "M":
                result = result.replace("%M", str(month))
            elif format_date[i+1] == "D":
                result = result.replace("%D", str(day))
            elif format_date[i+1] == "h":
                result = result.replace("%h", str(hour))
            elif format_date[i+1] == "m":
                result = result.replace("%m", str(minute))
            elif format_date[i+1] == "s":
                result = result.replace("%s", str(int(float(second))))

    return result


def parse_date(date):
    """
    :param str date:
    :return datetime.datetime:
    """
    Y, M, D, h, m, s = date.split()
    return datetime.datetime(int(Y), int(M), int(D), int(h), int(m), int(float(s)))

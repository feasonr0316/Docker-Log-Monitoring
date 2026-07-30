def detect_error(log):

    result = {

        "is_error": False,

        "reason": None,

        "level": "INFO"

    }


    # HTTP状态检测

    status = log.get("status")


    if status and status >= 400:

        result["is_error"] = True

        result["reason"] = f"HTTP status {status}"

        result["level"] = "HIGH"


        return result



    # 关键词检测

    message = log.get("message")


    if message:

        keywords = [

            "error",

            "failed",

            "exception",

            "warning",

            "critical"

        ]


        for word in keywords:

            if word.lower() in message.lower():

                result["is_error"] = True

                result["reason"] = f"keyword {word}"

                result["level"] = "MEDIUM"


                return result



    return result

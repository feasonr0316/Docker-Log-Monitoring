from detector import detect_error


log = {

    "container":"test-nginx",

    "status":500,

    "message":"Internal Server Error"

}


result = detect_error(log)


print(result)

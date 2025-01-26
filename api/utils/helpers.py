
# Response dict
def res_gen(data, status, message):
    return {
        'status': status,
        'message': message,
        'data': data
    }
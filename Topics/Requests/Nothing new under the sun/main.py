def database_manipulator():
    if request.method == 'PUT':
        return 'Updated'
    return "Deleted"

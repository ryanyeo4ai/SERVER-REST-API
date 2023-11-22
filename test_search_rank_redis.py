import redis

r = redis.Redis("localhost")
print(r.ping())

i = 1
while i <6:
    email = r.get('email_' + str(i))
    point = r.get('point_' + str(i))
    decoded_email = email.decode('utf-8')
    decoded_point = point.decode('utf-8')
    print(f'{decoded_email} : {decoded_point}')
    #print(type(email))
    i += 1
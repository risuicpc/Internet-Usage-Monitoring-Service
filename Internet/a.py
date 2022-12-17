f = open("user.txt", 'r')
a = ["username","MAC","start_time","usage_time","upload","download"]
ff = open("user_internet_initial_data.json", 'w')
ff.write("[\n")
id = 1
for i in f.readlines():
    i = i.strip().split(',')
    ff.write("    {\n")
    ff.write('        "model": "Internet.UserInternetIession",\n')
    ff.write('        "pk": '+str(id)+',\n')
    ff.write('        "fields": {\n')
    for j in range(6):
        if a[j] in ["upload","download"]:
            ff.write('            "'+a[j]+'": '+i[j])
            if a[j] == 'upload':
                ff.write(',')
            ff.write('\n')
        else:
            ff.write('            "'+a[j]+'": "'+i[j]+'",\n')
    ff.write("        }\n")
    ff.write("    },\n")
    id += 1
ff.write("]\n")


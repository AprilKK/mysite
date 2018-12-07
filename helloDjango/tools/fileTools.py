def handle_upload_file(file):
    with open('./helloDjango/articals/'+file.name,'wb+') as dest:
        for chunk in file.chunks():
            dest.write(chunk)
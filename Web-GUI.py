import os
import keystoneclient
import swiftclient
import gnupg
import sys
import json
from flask import Flask, render_template,request, redirect
app = Flask(__name__)



@app.route("/")
def hello():
    return "<h1 style='color:red;'>Hello</h1> <br> <br> <br> click on below links for respective uses <br> <br> Upload File : <a href = 'http://127.0.0.1:5000/upload'>http://127.0.0.1:5000/upload</a> <br> Container upload : <a href = 'http://127.0.0.1:5000/uploadContainer'>http://127.0.0.1:5000/uploadContainer</a> <br> File download : <a href = 'http://127.0.0.1:5000/download'>http://127.0.0.1:5000/download</a> <br> File Delete : <a href = 'http://127.0.0.1:5000/delete'>http://127.0.0.1:5000/delete</a><br> Container Delete : <a href = 'http://127.0.0.1:5000/deleteContainer'>http://127.0.0.1:5000/deleteContainer</a><br> Display Files : <a href = 'http://127.0.0.1:5000/displayFiles'>http://127.0.0.1:5000/displayFiles</a><br> <br>"

@app.route("/msg")
def msg():
    return 'upload the right size file'

@app.route("/user/<username>")
def user(username):
    return render_template('Web-GUI-Html.html', name=username)






@app.route("/uploadContainer")
def uploadContainer():
    return render_template('uploadContainer.html')



@app.route("/uploadContainerPost", methods=['POST'])
def uploadContainerPost():
    auth_url = "https://identity.open.softlayer.com/" + '/v3'
    project_id = "961c22402c7949898e8d3f33885486aa"
    user_id = "de3b0b49f6df4173ae9d81b457f8f34c"
    region_name = "dallas"
    password = "Hnfpl.T*G^1(60fD"
    conn = swiftclient.client.Connection(key=password,authurl=auth_url,auth_version='3',os_options={"project_id":project_id,"user_id":user_id,"region_name":region_name})

    
    container_name = request.form['container_name']
    conn.put_container(container_name)
    print("Container %s created successfully" %container_name)
    return redirect('/')
    




@app.route("/upload")
def upload():
    auth_url = "https://identity.open.softlayer.com/" + '/v3'
    project_id = "961c22402c7949898e8d3f33885486aa"
    user_id = "de3b0b49f6df4173ae9d81b457f8f34c"
    region_name = "dallas"
    password = "Hnfpl.T*G^1(60fD"
    conn = swiftclient.client.Connection(key=password,authurl=auth_url,auth_version='3',os_options={"project_id":project_id,"user_id":user_id,"region_name":region_name})


    containerList = []
    # List your containers
    print("\nContainer List:")
    for container in conn.get_account()[1]:
        print(container['name'])
        containerList.append(container['name'])


    return render_template('upload.html', data = containerList)





@app.route('/uploadFile', methods=['POST'])
def uploadFile():
    file_name = request.form['file_name']

    auth_url = "https://identity.open.softlayer.com/" + '/v3'
    project_id = "961c22402c7949898e8d3f33885486aa"
    user_id = "de3b0b49f6df4173ae9d81b457f8f34c"
    region_name = "dallas"
    password = "Hnfpl.T*G^1(60fD"
    conn = swiftclient.client.Connection(key=password,authurl=auth_url,auth_version='3',os_options={"project_id":project_id,"user_id":user_id,"region_name":region_name})

    container_name = request.form['container_name']
    #check for the file size
    size = os.path.getsize("example_file.txt")
    print(size)

    #if (size > 1000000) and (size < 10000000):
    if (size > 10) and (size < 100000):


        #Generate encryption key
        ##os.system('rm -rf /home/testgpguser/gpghome')
        ##gpg = gnupg.GPG(gnupghome='/home/testgpguser/gpghome')
        gpg = gnupg.GPG(gnupghome='C:\\Python33\\Lib\\site-packages\\gnupg')
        input_data = gpg.gen_key_input(key_type="RSA",
                                       key_length=1024,
            passphrase='Testing')
        key = gpg.gen_key(input_data)
        print(key)


        #encrypt the file
        with open(file_name, 'r') as example_encrypt_file:
            status = gpg.encrypt_file(example_encrypt_file,str(key),output='my-encrypted.txt.gpg')
        print('ok: ', status.ok)
        print('status: ', status.status)
        print('stderr: ', status.stderr)

        encrypted_file_name = 'my-encrypted.txt.gpg'

        # Create a file for uploading
        with open(encrypted_file_name, 'r') as example_file:
            conn.put_object(container_name, encrypted_file_name,
                                                contents= example_file.read(),
                                                content_type='text/plain')


        return redirect('/')
    else:
        return redirect('/msg')


@app.route("/delete")
def delete():
    auth_url = "https://identity.open.softlayer.com/" + '/v3'
    project_id = "961c22402c7949898e8d3f33885486aa"
    user_id = "de3b0b49f6df4173ae9d81b457f8f34c"
    region_name = "dallas"
    password = "Hnfpl.T*G^1(60fD"
    conn = swiftclient.client.Connection(key=password,authurl=auth_url,auth_version='3',os_options={"project_id":project_id,"user_id":user_id,"region_name":region_name})


    containerList = []
    # List your containers
    print("\nContainer List:")
    for container in conn.get_account()[1]:
        print(container['name'])
        containerList.append(container['name'])


    return render_template('delete.html', data = containerList)


@app.route('/deleteFile', methods=['POST'])
def deleteFile():
    file_name = request.form['file_name']

    auth_url = "https://identity.open.softlayer.com/" + '/v3'
    project_id = "961c22402c7949898e8d3f33885486aa"
    user_id = "de3b0b49f6df4173ae9d81b457f8f34c"
    region_name = "dallas"
    password = "Hnfpl.T*G^1(60fD"
    conn = swiftclient.client.Connection(key=password,authurl=auth_url,auth_version='3',os_options={"project_id":project_id,"user_id":user_id,"region_name":region_name})

    container_name = request.form['container_name']


    ### Delete an object
    conn.delete_object(container_name, file_name)
    print("\nObject %s deleted successfully." % file_name)

    return redirect('/')


@app.route("/deleteContainer")
def deleteContainer():
    auth_url = "https://identity.open.softlayer.com/" + '/v3'
    project_id = "961c22402c7949898e8d3f33885486aa"
    user_id = "de3b0b49f6df4173ae9d81b457f8f34c"
    region_name = "dallas"
    password = "Hnfpl.T*G^1(60fD"
    conn = swiftclient.client.Connection(key=password,authurl=auth_url,auth_version='3',os_options={"project_id":project_id,"user_id":user_id,"region_name":region_name})


    containerList = []
    # List your containers
    print("\nContainer List:")
    for container in conn.get_account()[1]:
        print(container['name'])
        containerList.append(container['name'])


    return render_template('deleteContainer.html', data = containerList)
    
@app.route("/deleteConatinerPost", methods=['POST'])
def deleteConatinerPost():
    auth_url = "https://identity.open.softlayer.com/" + '/v3'
    project_id = "961c22402c7949898e8d3f33885486aa"
    user_id = "de3b0b49f6df4173ae9d81b457f8f34c"
    region_name = "dallas"
    password = "Hnfpl.T*G^1(60fD"
    conn = swiftclient.client.Connection(key=password,authurl=auth_url,auth_version='3',os_options={"project_id":project_id,"user_id":user_id,"region_name":region_name})

    container_name = request.form['container_name']
    # To delete a container. Note: The container must be empty!
    conn.delete_container(container_name)
    print("\nContainer %s deleted successfully.\n" % container_name)

    return redirect('/')


@app.route("/download")
def download():
    auth_url = "https://identity.open.softlayer.com/" + '/v3'
    project_id = "961c22402c7949898e8d3f33885486aa"
    user_id = "de3b0b49f6df4173ae9d81b457f8f34c"
    region_name = "dallas"
    password = "Hnfpl.T*G^1(60fD"
    conn = swiftclient.client.Connection(key=password,authurl=auth_url,auth_version='3',os_options={"project_id":project_id,"user_id":user_id,"region_name":region_name})


    containerList = []
    # List your containers
    print("\nContainer List:")
    for container in conn.get_account()[1]:
        print(container['name'])
        containerList.append(container['name'])


    return render_template('download.html', data = containerList)


@app.route('/downloadFile', methods=['POST'])
def downloadFile():
    encrypted_file_name = request.form['file_name']

    auth_url = "https://identity.open.softlayer.com/" + '/v3'
    project_id = "961c22402c7949898e8d3f33885486aa"
    user_id = "de3b0b49f6df4173ae9d81b457f8f34c"
    region_name = "dallas"
    password = "Hnfpl.T*G^1(60fD"
    conn = swiftclient.client.Connection(key=password,authurl=auth_url,auth_version='3',os_options={"project_id":project_id,"user_id":user_id,"region_name":region_name})

    container_name = request.form['container_name']


    #Generate encryption key
    ##os.system('rm -rf /home/testgpguser/gpghome')
    ##gpg = gnupg.GPG(gnupghome='/home/testgpguser/gpghome')
    gpg = gnupg.GPG(gnupghome='C:\\Python33\\Lib\\site-packages\\gnupg')
    input_data = gpg.gen_key_input(key_type="RSA",
                                   key_length=1024,
        passphrase='Testing')
    key = gpg.gen_key(input_data)
    print(key)


     # Download an object and save it to ./my_example.txt
    obj = conn.get_object(container_name, encrypted_file_name)
    with open('decrypted_file_name.txt', 'w') as my_example:
        print(obj)
        print(obj[1])
        my_example.write(str(obj[1].decode("utf-8")))
        print("\nObject %s downloaded successfully." % encrypted_file_name)

    #decryt the file
    with open('decrypted_file_name.txt', 'rb') as f:
        status = gpg.decrypt_file(f, passphrase='Testing', output='my-decrypted.txt')

    
    print('status: ', status.status)
    print('stderr: ', status.stderr)


    
    return redirect('/')




@app.route("/displayFiles")
def displayFiles():    

    auth_url = "https://identity.open.softlayer.com/" + '/v3'
    project_id = "961c22402c7949898e8d3f33885486aa"
    user_id = "de3b0b49f6df4173ae9d81b457f8f34c"
    
    region_name = "dallas"
    password = "Hnfpl.T*G^1(60fD"
    conn = swiftclient.client.Connection(key=password,authurl=auth_url,auth_version='3',os_options={"project_id":project_id,"user_id":user_id,"region_name":region_name})

    list = []
    for container in conn.get_account()[1]:
        for data in conn.get_container(container['name'])[1]:
            list.append(data['name'])
                

    return render_template('displayFiles.html', data = list)


##if __name__ == "__main__":
##    app.run(debug=True)


port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(debug=True)
	app.run(host='0.0.0.0', port=int(port))

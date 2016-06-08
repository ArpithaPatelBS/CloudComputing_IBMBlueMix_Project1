import os
import keystoneclient
import swiftclient
import gnupg


auth_url = "https://identity.open.softlayer.com/" + '/v3'
project_id = "961c22402c7949898e8d3f33885486aa"
user_id = "de3b0b49f6df4173ae9d81b457f8f34c"
region_name = "dallas"
password = "Hnfpl.T*G^1(60fD"
conn = swiftclient.client.Connection(key=password,authurl=auth_url,auth_version='3',os_options={"project_id":project_id,"user_id":user_id,"region_name":region_name})

#Generate encryption key
##os.system('rm -rf /home/testgpguser/gpghome')
##gpg = gnupg.GPG(gnupghome='/home/testgpguser/gpghome')
gpg = gnupg.GPG(gnupghome='C:\\Python33\\Lib\\site-packages\\gnupg')
input_data = gpg.gen_key_input(key_type="RSA",
                               key_length=1024,
    passphrase='Testing')
key = gpg.gen_key(input_data)
print(key)


container_name = "new-container"
file_name = "example_file.txt"


#check for the file size
size = os.path.getsize("example_file.txt")
print(size)

#if (size > 1000000) and (size < 10000000):
if (size > 10) and (size < 100000):

    #Create a new container
    conn.put_container(container_name)
    print("Container %s created successfully" %container_name)

    # List your containers
    print("\nContainer List:")
    for container in conn.get_account()[1]:
        print(container['name'])


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

    # List objects in a container, and prints out each object name, the file size, and last modified date
    print ("\nObject List:")
    for container in conn.get_account()[1]:
        for data in conn.get_container(container['name'])[1]:
            print('object: {0}\t size: {1}\t date: {2}'.format(data['name'], data['bytes'], data['last_modified']))

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

    print('ok: ', status.ok)
    print('status: ', status.status)
    print('stderr: ', status.stderr)



    ### Delete an object
    ##conn.delete_object(container_name, file_name)
    ##print("\nObject %s deleted successfully." % file_name)
    ##
    ##
    ### To delete a container. Note: The container must be empty!
    ##conn.delete_container(container_name)
    ##print("\nContainer %s deleted successfully.\n" % container_name)

    
else:
    print("upload the right size file")

# بسم الله الرحمن الرحيم
# -*- coding: utf-8 -*-
import base64
import requests , json
from websocket import create_connection
import concurrent.futures


def r(id):
    return id[::-1]



def toenc(payload,id):
     # call me on telegram m7md1337


def todec(payload,id):
    # call me on telegram m7md1337



def sendwebsocket(id,proxy):
    global list2 ,version1
    pprrooxxy = proxy.replace("\n", "").split(':', 3)
    # host 0 port 1 username 2 password 3
    reversid = id[::-1]
    firstP= base64.b64encode(base64.b64encode(toenc('{"c":"i"}',reversid).encode()))
    ws = create_connection("wss://ws.strawpoll.com/polls/"+id+"",http_proxy_host=pprrooxxy[0],http_proxy_port=pprrooxxy[1],http_proxy_auth=(pprrooxxy[2],pprrooxxy[3]))
    ws.send(firstP)
    r = ws.recv()
    tk = json.loads(todec(base64.b64decode(base64.b64decode(r.decode())).decode(),reversid).replace('\u0002',''))
    secondP = r'{"c":"v","vi":"111111111111111111111","tk":"'+tk["tk"]+'","pv":"'+version1+'","v":{"id":null,"name":"","pollVotes":[' + ",".join(
        list2) + '],"otherOption":null,"voteType":"add"},"h":false}'
    secondP = base64.b64encode(base64.b64encode(toenc(secondP,reversid).encode()))
    ws.send(secondP)
    r = ws.recv().decode().replace("\n","")
    dep = todec(base64.b64decode(base64.b64decode(r).decode().replace('\n','')).decode(),reversid)
    #print(dep)
    if "You cannot vote on this poll anymore." in dep:
        raise ValueError("You cannot vote on this poll anymore the poll has been end.")
    elif "You (or someone in your Wi-Fi\/network) have already participated in this vote" in dep:
        raise ValueError("the ip its used before. ")
    elif "This poll has been changed in the meantime, please reload the page and vote again." in dep:
        raise ValueError("the poll settings has been change plz kill the script and start again")
    elif '"Thanks for your vote!","p"' in dep:# some res dose not have p value
        r = json.loads(todec(base64.b64decode(base64.b64decode(r).decode().replace('\n','')).decode(),reversid).replace('\u0004',''))
        return {"id":r['p'],"tk":r["tk"]}
    else:
        raise ValueError("i do not know whats the propblem \ error : ^^ " +dep +" ^^")



def httprequets(url,id,proxy):
    pprrooxxy = proxy.replace("\n","").split(':', 2)
    pprrooxxy= "https://"+pprrooxxy[2]+"@"+pprrooxxy[0]+":"+pprrooxxy[1]+""
    dd = json.dumps(sendwebsocket(id,proxy))
    dd = json.loads(dd)
    body = r'{"tk":"'+dd["tk"]+'","id":"'+dd["id"]+'"}'
    re = requests.post("https://api.strawpoll.com/v2/polls/"+id+"/save_vote",data=body,proxies={"https":pprrooxxy})
    if  "1" in re.text:
        print("Vote successful")
    else:
        print("error not voting")



if __name__ == '__main__':
    try:
        url = input("hi enter the url ex. https://strawpoll.com/polls/blablabla :")
        poxylistfile1 = input("enter proxy file :")
        poxylistfile1 = open(poxylistfile1, "r").read()
        id = url.rsplit('/', 1)
        re = requests.get("https://api.strawpoll.com/v2/polls/{}".format(id[1]))
        if re.status_code == 404:
            raise IndexError("plz enter an right url")
        data = json.loads(re.text)
        cont = 0
        version1 = data["poll"]["version"]
        list1 = []
        list2 = []
        for xx in data["poll"]["poll_options"]:
            list1.append(xx["value"])
            cont+=1
            print("number: "+str(cont) + "|"+ ' ' + xx['value'])
        numberanswer = int(input("please enter the number :"))
        numberanswer-=1
        for xx in range(cont):
            list2.append("0")
        list2[numberanswer]="1"
    except IOError:
        print("error : File not accessible")
        exit(0)
    except KeyError:
        print("error : plz enter an right url")
        exit(0)
    except IndexError:
        print("error : plz enter an right url")
        exit(0)
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(httprequets, url, id[1], prrooxx): prrooxx for prrooxx in poxylistfile1.splitlines()}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
            except ValueError as ss:
                print(ss)
            except Exception as exc:
                print("reason : "+str(exc)+" , when use proxy : "+str(url)+" ")

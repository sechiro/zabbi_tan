#!/usr/bin/python
# -*- coding: utf-8 -*
def main():
    import sys
    import re
    host = 'localhost'
    port = 9801
    message = ''
    
    trigger = sys.argv[1] # {HOSTNAME}:{TRIGGER.NAME}:{TRIGGER.SEVERITY}:{TRIGGER.VALUE}
    trigger_keys = trigger.split(':', 4)

    #print trigger_keys[4].decode('utf-8')
    trigger_keys[4] = trigger_keys[4].decode('shift-jis')
    #print trigger_keys[4]
    
    # kana or kayo
    if re.match('kana', trigger_keys[0]):
        # Error or Restored
        if re.match('1', trigger_keys[3]):
            trigger_keys[3] = 'PROBLEM'
            message = ur'\s[3]\_v[voice\3arekanachanno.mp3]あれ！？\w[1000]\nかなちゃんの調子がおかしくない？\n\n'

                
        elif re.match('0', trigger_keys[3]):
            trigger_keys[3] = 'OK'
            message = ur'\w[3]\s[1220]\_v[voice\3yokattafutaritomo.mp3]よかった。\w[700]二人とも元気になったみたい。\n\n'
            message += ur'\w[2500]\s[0]'
    
    elif re.match('kayo', trigger_keys[0]):
        # Error or Restored
        if re.match('1', trigger_keys[3]):
            trigger_keys[3] = 'PROBLEM'
            message = ur'\s[301]\_v[voice\3kyaakayochanga.mp3]きゃあ！\w[600]\nかよちゃんがー>_<\n\n\w[800]\s[7]なんとかしてよね。\n\n'

        elif re.match('0', trigger_keys[3]):
            trigger_keys[3] = 'OK'
            message = ur'\w[3]\s[1220]\_v[voice\3yokattafutaritomo.mp3]よかった。\w[700]二人とも元気になったみたい。\n\n'
            message += ur'\w[2500]\s[0]'


    # General Trigger
    else:
        # Error or Restored
        if re.match('1', trigger_keys[3]):
            trigger_keys[3] = 'PROBLEM'
            
            if re.match('Disaster', trigger_keys[2]):
                message = ur'\s[301]\_v[voice\4nandekonnani.mp3]なんでこんなになるまで放っておいたの！？\w[1200]\n…\s[4]もう…ダメかもしれない…\w[3000]\s[104]\n\n'
            elif re.match('High', trigger_keys[2]):
                message = ur'\s[300]\_v[voice\4douyaramazuikoto.mp3]どうやらマズいことになったみたいね…\w[1400]\n\s[400]いい？ 絶対治すのよ。\n\n\w[1600]\s[1402]信じてるわ。\w[3000]\s[207]\n\n'            
            elif re.match('Average', trigger_keys[2]):
                message = ur'\s[300]\_v[voice\4sukosisyougai.mp3]少し障害が出てるみたい。\w[1000]\n\s[422]そろそろ\w[700]あなたの腕を見せてもらおうかしら。\n\n'
                message += ur'\w[2500]\s[0]'
            elif re.match('Warning', trigger_keys[2]):
                message = ur'\s[310]\_v[voice\4kikennachoko.mp3]危険な兆候ね…\w[1000]\n\n\s[420]くれぐれも\w[700]監視を怠らないこと！\n\n'
                message += ur'\w[2500]\s[0]'
            elif re.match('Information', trigger_keys[2]):
                message = ur'\s[310]\_v[voice\4iyanayokanga.mp3]嫌な予感がするわ…\w[1400]\n\n\わたしの思いすごしならいいんだけど。\n\n'
                message += ur'\w[2500]\s[0]'
            elif re.match('Not classified', trigger_keys[2]):
                message = ur'\s[1100]\_v[voice\4nandemonai.mp3]なんでもない。\w[1000]\n\s[1120]ただ\w[700]呼んでみただけ。\n\n'
                message += ur'\w[2500]\s[0]'


        elif re.match('0', trigger_keys[3]):
            trigger_keys[3] = 'OK'
            
            if re.match('Disaster', trigger_keys[2]):
                message = ur'\s[311]\_v[voice\4kusun2.mp3]（ぐすっ）\w[1000]\s[200]えっ！？\w[2600]\n本当に治ったの…\n\n\w[3000]\s[1]あ、\w[300]ありがとう。\w[3000]見直したわ。\n\w[2000]これからも\w[1500]\s[1230]よろしくね。\n\n'
                message += ur'\w[4500]\s[0]'
            elif re.match('High', trigger_keys[2]):
                message = ur'\s[130]\_v[voice\4syougaikarakaifuku.mp3]障害から回復したようね。\w[1400]\n\n\s[1200]あ、あなたにしてはよくやったわ。\n\w[3000]\s[1221]お疲れさま。\n\n'
                message += ur'\w[5500]\s[0]'
            elif re.match('Average', trigger_keys[2]):
                message = ur'\s[203]\_v[voice\4moudaijoubu.mp3]もう大丈夫みたいね。\w[1400]\n\n…\s[1210]まあ、この程度は直せて当然かしら。\n\n'
                message += ur'\w[4500]\s[0]'
            elif re.match('Warning', trigger_keys[2]):
                message = ur'\s[6]\_v[voice\4hitomazukikenwa.mp3]ひとまず危険は去ったみたい。\w[1000]\n\s[400]引き続き、\w[700]気を締めていくわよ。\n\n'
                message += ur'\w[2500]\s[0]'
            elif re.match('Information', trigger_keys[2]):
                message = ur'\s[6]\_v[voice\4hitomazukikenwa.mp3]ひとまず危険は去ったみたい。\w[1000]\n\s[400]引き続き、\w[700]気を締めていくわよ。\n\n'
                message += ur'\w[2500]\s[0]'
            elif re.match('Not classified', trigger_keys[2]):
                message = ur'\s[1100]\_v[voice\4nandemonai.mp3]なんでもない。\w[1000]\n\s[1120]ただ\w[700]呼んでみただけ。\n\n'
                message += ur'\w[2500]\s[0]'

       
    # フッターなどをつけて、送信。
    medium = ':'
    message += medium.join(trigger_keys) # 表示するトリガを組立て直す。
    message += ur'\e'
    ghost_name = u'ざびたん'
    request = sstp_send_request(message, ghost_name)
    send_sstp(host, port, request)

def sstp_send_request(message, ghost_name=u'test-agent'):
    request = u'SEND SSTP/1.4\r\n'
    request += u'Sender: ' + ghost_name + u'\r\n'
    request += u'Script: ' + message + u'\r\n' 
    request += u'Charset: UTF8\r\n'
    return request


def send_sstp(host, port, request):
    """send socket"""
    import socket

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send(request.encode('utf-8'))
    s.close()
    

if __name__ == '__main__':
    main()

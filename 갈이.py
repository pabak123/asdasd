import discord
import asyncio
from discord import Client
from bs4 import BeautifulSoup
import requests
import urllib
import openpyxl
from captcha.image import ImageCaptcha
import random
import time


client: Client = discord.Client()


@client.event
async def on_ready():
    print("봇이 성공적으로 실행되었습니다.")
    game = discord.Game('도움 주는 척')
    await client.change_presence(status=discord.Status.online, activity=game)



@client.event
async def on_message(message):
    global selcolor
    if message.content.startswith('상갈아 핑'):
        await message.delete()
        embed = discord.Embed(description=f"", colour=discord.Colour(0x594841))
        embed.set_author(name=f"현재 핑은 {int((client.latency * 1000))}'ms 입니다.")
        await message.channel.send(embed=embed)
    if message.content.startswith('상갈아 뮤트'):
        if message.author.guild_permissions.manage_messages:
            reason = message.content[30:]

            if reason == '':
                reason = 'None'
            else:
                pass

            await message.delete()
            await message.channel.set_permissions(message.mentions[0], read_messages=True, send_messages=False)

            embed1 = discord.Embed(title='', description=(f'**사유 : ** ``{reason}``'))
            embed1.set_author(name=f'{message.mentions[0].name} 님을 뮤트 하였습니다.',
                              icon_url=(client.get_user(int(message.mentions[0].id)).avatar_url))
            await message.channel.send(embed=embed1)

    if message.content.startswith('상갈아 언뮤트'):
        if message.author.guild_permissions.manage_messages:
            await message.delete()
            await message.channel.set_permissions(message.mentions[0], read_messages=True, send_messages=True)

            embed1 = discord.Embed(title='', description=(''))
            embed1.set_author(name=f'{message.mentions[0].name} 님을 언뮤트 하였습니다.',
                              icon_url=(client.get_user(int(message.mentions[0].id)).avatar_url))
            await message.channel.send(embed=embed1)

    if message.content.startswith("상갈아 인증"): #명령어 /인증
        a = ""
        Captcha_img = ImageCaptcha()
        for i in range(6):
            a += str(random.randint(0, 9))

        name = str(message.author) + ".png"
        Captcha_img.write(a, name)

        await message.channel.send(f"""{message.author.mention} 아래 숫자를 10초 내에 입력해주세요. """)
        await message.channel.send(file=discord.File(name))

        def check(msg):
            return msg.author == message.author and msg.channel == message.channel

        try:
            msg = await client.wait_for("message", timeout=10, check=check) # 제한시간 10초
        except:
            await message.channel.purge(limit=3)
            chrhkEmbed = discord.Embed(title='❌ 인증실패', color=0xFF0000)
            chrhkEmbed.add_field(name='닉네임', value=message.author, inline=False)
            chrhkEmbed.add_field(name='이유', value='시간초과', inline=False)
            await message.channel.send(embed=chrhkEmbed)
            print(f'{message.author} 님이 시간초과로 인해 인증을 실패함.')
            return

        if msg.content == a:
            role = discord.utils.get(message.guild.roles, name="상갈동 인간들")
            await message.channel.purge(limit=4)
            tjdrhdEmbed = discord.Embed(title='인증성공', color=0x04FF00)
            tjdrhdEmbed.add_field(name='닉네임', value=message.author, inline=False)
            tjdrhdEmbed.add_field(name='5초후 인증역할이 부여됩니다.', value='** **', inline=False)
            tjdrhdEmbed.set_thumbnail(url=message.author.avatar_url)
            await message.channel.send(embed=tjdrhdEmbed)
            time.sleep(5)
            await message.author.add_roles(role)
        else:
            await message.channel.purge(limit=4)
            tlfvoEmbed = discord.Embed(title='❌ 인증실패', color=0xFF0000)
            tlfvoEmbed.add_field(name='닉네임', value=message.author, inline=False)
            tlfvoEmbed.add_field(name='이유', value='잘못된 숫자', inline=False)
            await message.channel.send(embed=tlfvoEmbed)
            print(f'{message.author} 님이 잘못된 숫자로 인해 인증을 실패함.')

    if message.content.startswith('상갈아배워'):
        file = openpyxl.load_workbook('log.xlsx')
        work = message.content.split(' ')
        sheet = file.active
        for i in range(1, 51):
            if sheet['A' + str(i)].value == '-' or sheet['A' + str(i)].value == work[1]:
                sheet['A' + str(i)].value = work[1]
                sheet['B' + str(i)].value = work[2]
                sheet['C' + str(i)].value = message.author.name
                embed = discord.Embed(colour=discord.Colour(0x7C77FF))
                embed.set_author(name=f'이제 {work[1]} 이라고 말하면 {work[2]} 라고 말할게요.')
                await message.channel.send(embed=embed)
                break
        file.save('log.xlsx')

    if message.content.startswith(''):
        file = openpyxl.load_workbook('log.xlsx')
        work = message.content
        sheet = file.active
        for i in range(1, 51):
            if sheet['A' + str(i)].value == work:
                await message.channel.send(
                    sheet['B' + str(i)].value )
                break

    if message.content.startswith("집합"):
        await message.channel.send("네")


    if message.content.startswith("상갈아 출근"):
        try:
            # 메시지 관리 권한 있을시 사용가능
            if message.author.guild_permissions.manage_messages:
                embed = discord.Embed(color=0x80E12A)
                channel = 793347285719056404
                embed.set_author(name=message.author, icon_url=message.author.avatar_url)
                embed.add_field(name='관리자 출퇴근 알림', value='관리자가 출근하였습니다.')
                # embed.set_image(url="")
                await client.get_channel(int(channel)).send(embed=embed)
        except:
            pass

    if message.content.startswith('상갈아 한강온도'):
        json = requests.get('http://hangang.dkserver.wo.tc/').json()
        temp = json.get("temp") # 한강온도
        time = json.get("time") # 측정시간

        embed = discord.Embed(title='💧 한강온도', description=f'{temp}°C', colour=discord.Colour.blue())
        embed.set_footer(text=f'{time}에 측정됨')

        await message.channel.send(embed=embed)

    if message.content.startswith("상갈아 퇴근"):
        try:
            if message.author.guild_permissions.manage_messages:
                embed = discord.Embed(color=0xFF0000)
                channel = 793347285719056404
                embed.set_author(name=message.author, icon_url=message.author.avatar_url)
                embed.add_field(name='관리자 출퇴근 알림', value='관리자가 퇴근하였습니다.')
                # embed.set_image(url="")
                await client.get_channel(int(channel)).send(embed=embed)
        except:
            pass

    if message.content.startswith('상갈아 코로나'):
        url = 'http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=11&ncvContSeq=&contSeq=&board_id=&gubun='
        html = urllib.request.urlopen(url)
        soup = BeautifulSoup(html, "html.parser")

        datecr = soup.find('span', {'class': 't_date'})  # 기준날짜
        # print(f'기준일: {datecr.string}')

        totalcovid = soup.select('dd.ca_value')[0].text  # 누적 확진자수
        # print(f'누적 확진자: {totalcovid} 명')

        todaytotalcovid = soup.select('p.inner_value')[0].text  # 당일 확진자수 소계
        # print(f'확진자 소계: {todaytotalcovid} 명')

        todaydomecovid = soup.select('p.inner_value')[1].text  # 당일 국내발생 확진자수
        # print(f'국내발생: {todaydomecovid} 명')

        todayforecovid = soup.select('p.inner_value')[2].text  # 당일 해외유입 확진자수
        # print(f'해외유입: {todayforecovid} 명')

        totalca = soup.select('dd.ca_value')[2].text  # 누적 격리해제
        # print(f'누적 격리해제: {totalca} 명')

        todayca = soup.select('span.txt_ntc')[0].text  # 당일 격리해제
        # print(f'격리해제: {todayca} 명')

        totalcaing = soup.select('dd.ca_value')[4].text  # 누적 격리중
        # print(f'누적 격리중: {totalcaing}')

        todaycaing = soup.select('span.txt_ntc')[1].text  # 당일 격리중
        # print(f'격리중: {todaycaing} 명')

        totaldead = soup.select('dd.ca_value')[6].text  # 누적 사망자
        # print(f'누적 사망자: {totaldead} 명')

        todaydead = soup.select('span.txt_ntc')[2].text  # 당일 사망자
        # print(f'사망자: {todaydead} 명')

        covidembed = discord.Embed(title='코로나19 국내 발생현황', description="", color=0xFF0F13, url='http://ncov.mohw.go.kr/')
        covidembed.add_field(name='🦠 확진환자', value=f'{totalcovid}({todaytotalcovid}) 명'
                                                   f'\n\n국내발생: {todaydomecovid} 명\n해외유입: {todayforecovid} 명',
                             inline=False)
        covidembed.add_field(name='😷 격리중', value=f'{totalcaing}({todaycaing}) 명', inline=False)
        covidembed.add_field(name='🆓 격리해제', value=f'{totalca}({todayca}) 명', inline=False)
        covidembed.add_field(name='💀 사망자', value=f'{totaldead}({todaydead}) 명', inline=False)
        covidembed.set_footer(text=datecr.string)
        await message.channel.send(embed=covidembed)

    if message.content.startswith('상갈아 청소'):
        try:
            # 메시지 관리 권한 있을시 사용가능
            if message.author.guild_permissions.manage_messages:
                amount = message.content[4:]
                await message.delete()
                await message.channel.purge(limit=int(amount))
                message = await message.channel.send(embed=discord.Embed(title='🧹 메시지 ' + str(amount) + '개 삭제됨', colour=discord.Colour.green()))
                await asyncio.sleep(2)
                await message.delete()
            else:
                await message.channel.send('``명령어 사용권한이 없습니다.``')
        except:
            pass
    
    if message.content.startswith('상갈아 실검'):
        json = requests.get('https://www.naver.com/srchrank?frm=main').json()
        ranks = json.get("data")
        data = []
        for r in ranks:
            rank = r.get("rank")
            keyword = r.get("keyword")
            if rank > 10:
                break
            data.append(f'**{rank}**위 {keyword}')

        dat = str(data)
        dat = dat.replace("'","")
        dat = dat.replace(", ","\n")
        dat = dat[1:-1]
        print(dat)
        embed = discord.Embed(title= '네이버 실시간 검색어 순위', description=(dat),colour=0x19CE60)
        await message.channel.send(embed=embed)
    
    if message.content.startswith('상갈아 도움'):
        embed = discord.Embed(title="상갈이의 명령어", description="상갈이에 대해 더 잘 알고 싶다고요? 아래 내용을 잘봐보세요!", color=0x62c1cc) # Embed의 기본 틀(색상, 메인 제목, 설명)을 잡아줍니다
        embed.add_field(name="상갈아 코로나", value="현재 코로나의 상태를 실시간으로 정보를 받아서 보여줘요!", inline=True)
        embed.add_field(name="상갈아 실검", value="사이트 네이버에서 실검 정보를 받아와 직접 보여줘요!", inline=True)
        embed.add_field(name="상갈아 한강온도", value="한강온도를 직접 재 줘요! 혹시.. 자살하시려는 건 아니죠?", inline=True)
        embed.add_field(name="상갈아배워", value="띄어쓰기를 하지않고 붙여서 써주세요! 그래야 상갈이가 배운답니다!", inline=True)
        embed.add_field(name="상갈아 핑", value="현재 당신이 사용중인 Discord API 서버와의 연결 대기시간을 보여줘요!", inline=True)
        embed.set_footer(text="상갈") # 하단에 들어가는 조그마한 설명을 잡아줍니다
        await message.channel.send(embed=embed) # embed를 포함 한 채로 메시지를 전송합니다.


# 구동 할 봇 토큰
client.run("bot_token")

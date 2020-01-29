import datetime


class Getdays():
    def __init__(self):
        self.today = datetime.datetime.today().date()
        # 令和2年度福島県高校入試の日に設定
        self.day = str(datetime.datetime(2020, 3, 4).date() -
                       self.today)[:2].rstrip(" ")

        self.days = {
            0: "月曜日",
            1: "火曜日",
            2: "水曜日",
            3: "木曜日",
            4: "金曜日",
            5: "土曜日",
            6: "日曜日"
        }

        self.messages = {
            "0:": "いよいよ今日は入試の日ですね。\n今までやってきたことを思い出して、自信を持って挑みましょう！\nbyぽこまる",
            "5": "入試まで残り5日。\nたとえ最下位でも合格は合格。\nbyドラゴン桜",
            "10": "入試まで残り10日。\n試験は常に自分との戦い。\nbyドラゴン桜",
            "15": "入試まで残り15日。\n他人に促されなくても努力する人間が一番成長する。\nbyドラゴン桜",
            "20": "入試まで残り20日。\n自分で反省して立ち直る。そういう精神的な強さがなければ、受験では絶対に勝てない。\nbyドラゴン桜",
            "25": "入試まで残り25日。\n知らないことに挑戦し克服することが大事なんだ。\nbyドラゴン桜",
            "30": "入試まで残り30日。\n入試のプレッシャーに負けない自信。明確な根拠のある自信。それを得るためにはひたすら勉強するしかないのだ。\nbyドラゴン桜",
            "35": "入試まで残り35日。\nすぐに結果が出るわけではない そこで絶対投げ出さないこと。\nbyドラゴン桜",
            "40": "入試まで残り40日。\n基礎的な学習が、全ての根元であり、王道だ！\nbyドラゴン桜"
        }

    def return_day(self):
        if self.day in self.messages:
            return self.messages[self.day]
        else:
            return "高校入試まで残り" + self.day + "日です！"

    def return_precheck(self):
        return "勉強の進捗はどうでしょうか？\n今日もしっかりと23時59分までに学習状況を報告しましょう！"

    def return_check(self):
        day_data = self.today.weekday()
        today = str(self.today).replace("-", "")
        year = today[:4]
        month = today[4:6]
        day = today[6:8]
        return year + "年" + month + "月" + day + "日(" + self.days[day_data] + ")の学習状況を報告して下さい！"

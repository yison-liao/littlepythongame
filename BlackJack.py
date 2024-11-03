import random
import sys
import time


class BlackJack:
    """
    21點，與莊家對賭，所持手牌越接近21點越大，21點整勝，超過21點爆掉輸

    規則:
    1. 所有花色沒有大小需別
    2. 2~10 卡牌面值為其大小
    3. J、Q、K 均值10點
    4. A價值11點或1點
    5. 下注後，牌局開始
    6. 牌局開始時，你與莊家各有兩張牌，你可以選擇(H)it再拿一張牌、(S)tand停止拿牌、(D)ouble down 加注但是必須hit至少一次
    7. 和局則退回賭金
    """

    def __init__(self, bet_limit: int) -> None:
        self.bet_limit = bet_limit
        self.player_treasure_left = bet_limit
        self.handcards_number_limit = 5

    def game_on(self):
        print("Black Jack start!")
        while self.player_treasure_left > 0:
            print(f"Put your bet(1~{self.player_treasure_left}), or quit.")
            bet = self.get_bet()
            print(f"Player bet {bet} in this game.")
            # 洗牌->發牌
            cards_set: list = self.shuffle_cards()
            player_handcard = [cards_set.pop(0), cards_set.pop(0)]
            dealer_handcard = [cards_set.pop(0), cards_set.pop(0)]
            print("Dealer's hand:")
            self.show_handcard(dealer_handcard, half=True)
            print("Your hand:")
            self.show_handcard(player_handcard)

            # Hit、Stand、Double down?
            while (len(player_handcard) < self.handcards_number_limit) and (
                self.get_face_value(player_handcard) < 21
            ):
                print("What are you going to do? (H)it、(S)tand or (D)ouble down")
                move = input("-> ").strip().lower()
                if move.startswith("s"):
                    break
                elif move.startswith("h"):
                    player_handcard.append(cards_set.pop(0))
                    self.show_handcard(player_handcard)

                elif move.startswith("d"):
                    print("How much you want to increase?")
                    bet += self.get_bet()
                    player_handcard.append(cards_set.pop(0))
                    self.show_handcard(player_handcard)
                else:
                    print("Error input")
            # 與莊家對決
            self.compete(player_handcard, dealer_handcard, bet, cards_set)
            if self.player_treasure_left <= 0:
                print("You broke bro~ , don't gamble. It does not suit you.")
            print("Continue or not? (y/n)")
            choice = input("-> ").lower()
            if choice.startswith("n"):
                print("Expect your coming next time.")
                break
        else:
            print("You have already ran out of bet!!")
            print("Game over!!")

    def get_bet(self):
        if self.player_treasure_left <= 0:
            print("You have already ran out of bet!!")
            return 0
        print("How much you want to bet or (Q)uit?")
        bet = input("-> ")
        if bet.isdecimal():
            self.player_treasure_left -= int(bet)
            return int(bet)
        else:
            print("Game over!!")
            sys.exit()

    def shuffle_cards(self):
        RANK = [chr(9824), chr(9827), chr(9829), chr(9830)]  # 花色
        FACE = [val for val in range(2, 11)] + ["A", "J", "Q", "K"]
        cards = []
        for color in RANK:
            for val in FACE:
                cards.append((val, color))
        random.shuffle(cards)

        return cards

    def show_handcard(self, handcard: list, half=False):
        # picturize the card
        def card_fig(card: tuple) -> list:
            fig = ["", "", ""]
            fig[0] = f"|{card[0]}　　" + "|"
            fig[1] = f"|　{card[1]}　"
            fig[2] = f"|　　{card[0]}" + "|"
            if len(str(card[0])) == 2:
                fig[1] += " |"
            else:
                fig[1] += "|"
            return fig

        # assemble cards to demo
        handcard_pic = []
        for idx, card in enumerate(handcard):
            if idx == 0 and half is True:
                handcard_pic.append(card_fig(("#", "#")))
            else:
                handcard_pic.append(card_fig(card))
        for line in range(3):
            row = ""
            for pic in handcard_pic:
                row += pic[line]
            print(row)

    def compete(
        self, player_handcard: list, dealer_handcard: list, bet: int, cards_set: list
    ):
        player_face_value = self.get_face_value(player_handcard)

        dealer_face_value = self.dealer_decision(
            dealer_handcard, player_face_value, cards_set
        )  # 莊家對自己的牌面做增減

        if player_face_value > dealer_face_value:
            self.player_treasure_left += 2 * bet
            print(f"You won the bet: {bet}")
            print(f"Your treasure increase to {self.player_treasure_left}")
        elif player_face_value == dealer_face_value:
            print("Tied! Return your bet.")
            self.player_treasure_left += bet
            print(f"Your treasure left {self.player_treasure_left}")
        else:
            print("You lose!!!")
            print(f"Your treasure left {self.player_treasure_left}")

    def get_face_value(self, handcard: list[tuple]):
        value_parser = {"J": 10, "Q": 10, "K": 10}  # "A": [1, 11],
        face_value = [card[0] for card in handcard]
        if (
            any([key in face_value for key in value_parser.keys()] + [10 in face_value])
            is True
        ):
            if "A" in face_value:
                face_value[face_value.index("A")] = 11
            for value in face_value:
                if value in value_parser.keys():
                    face_value[face_value.index(value)] = value_parser[value]
        else:
            while "A" in face_value:
                face_value[face_value.index("A")] = 1

        return sum(face_value) if sum(face_value) <= 21 else 0

    def dealer_decision(
        self, handcard: list[tuple], player_face_value: int, cards_set: list[tuple]
    ):
        diff = 3
        """
        在確定玩家stand之後，dealer根據自己的手牌決定要不要hit
        設定一些參數: 當face_vale <= 21-diff，dealer stand
        """
        if player_face_value == 0:
            return self.get_face_value(handcard)
        elif player_face_value == 21:
            diff = 0

        while 0 < self.get_face_value(handcard) < (21 - diff):
            handcard.append(cards_set.pop(0))
            time.sleep(0.5)
            print("Dealer goes~")
            self.show_handcard(handcard)

        return self.get_face_value(handcard)


if __name__ == "__main__":
    bj = BlackJack(5000)
    # cardset = bj.shuffle_cards()
    # dealer = [cardset.pop(0), cardset.pop(0)]
    # bj.dealer_decision(dealer, cardset)

    bj.game_on()

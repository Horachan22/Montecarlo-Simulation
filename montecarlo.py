'''
===================================================================
Project Name  : 電子デバイス モンテカルロシミュレーション
File Name     : montecarlo.py
Encoding      : UTF-8
Creation Date : 25/6/2021
Copyright (c) 2021 Yuma Horaguchi All rights reserved.
===================================================================
'''

import numpy as np
import os
import time
import random
import pygame
from pygame.locals import *
import math
import sys

#一辺の設定
N = 5

pygame.init()
# (0) 各要素の決定
data = np.random.randint(0, 360, (N, N))
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FONT = pygame.font.Font('NotoSerifJP-Regular.otf', 30)
SCREEN = pygame.display.set_mode((500, 550))
y_offset = 50
ARROW = FONT.render('→', True, BLACK)

class Block(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self, self.containers)
		self.rect.left = SCREEN.left + x * self.rect.width
		self.rect.top = SCREEN.top + y * self.rect.height

def display_screen():
	text = FONT.render('Montecarlo Simulation', True, WHITE)
	SCREEN.fill(BLACK)
	text_rect = text.get_rect()
	text_rect.center = (250, 25)
	SCREEN.blit(text, text_rect)
	for i in range(N):
		for j in range(N):
			size = 500 / N
			x = i * size
			y = j * size + y_offset
			pygame.draw.rect(SCREEN, WHITE, (x, y, size - 1, size - 1))

			arrow = pygame.transform.rotate(ARROW, data[j][i])
			arrow_rect = arrow.get_rect()
			arrow_rect.center = (x + size / 2, y + size / 2)
			SCREEN.blit(arrow, arrow_rect)
	pygame.display.update()

def get_inner_product(angle_1 : int, angle_2 : int) -> float:
	return np.cos((angle_1 - angle_2) * np.pi / 180)

def get_energy(x : int, y : int) -> float:
	# 左右の要素との内積の和LRと、上下との内積の和UD
	LR = 0
	UD = 0
	# 抽出要素が上端の場合(=上との内積なし)
	if x == 0:
		UD = get_inner_product(data[x][y], data[x + 1][y])
	# 抽出要素が下端の場合(=下との内積なし)
	elif x == N - 1:
		UD = get_inner_product(data[x - 1][y], data[x][y])
	else:
		UD = get_inner_product(data[x][y], data[x + 1][y]) + get_inner_product(data[x - 1][y], data[x][y])
	# 抽出要素が左端の場合(=左との内積なし)
	if y == 0:
		LR = get_inner_product(data[x][y], data[x][y + 1])
	# 抽出要素が右端の場合(=右との内積なし)
	elif y == N - 1:
		LR = get_inner_product(data[x][y - 1], data[x][y])
	else:
		LR = get_inner_product(data[x][y], data[x][y + 1]) + get_inner_product(data[x][y - 1], data[x][y])
	return LR + UD

def judge_end(data) -> bool:
	mini = min([j for i in data for j in i])
	maxi = max([j for i in data for j in i])
	#厳密解
	# if maxi - mini != 0:
	# 	return False
	# 実行時間短縮のためのコード
	if maxi - mini > 1:
		return False
	return True

def main():
	pygame.display.set_caption("電子デバイス_モンテカルロシミュレーション")
	running = True #メインループ
	while running and judge_end(data) != True:
		display_screen()
		clock.tick(100)
		# (1) S_{i,j}の抽出
		i = np.random.randint(0, N)
		j = np.random.randint(0, N)
		# (2) θ'を変化させる
		origin = data[i][j] #θ控え
		option = np.random.randint(0, 360) #θ'
		# (3) エネルギーの計算
		former = get_energy(i,j) #変更前のエネルギー
		data[i][j] = option #変更
		latter = get_energy(i,j) #変更後のエネルギー
		if latter < former: #エネルギー的に不安定の場合
			data[i][j] = origin #元に戻す
		os.system('clear')
		print(data)
		#終了
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
				pygame.quit()
				sys.exit()

if __name__ == '__main__':
	main()

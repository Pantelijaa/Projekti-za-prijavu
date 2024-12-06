import random
import pyautogui
import sys
import time
from pynput.keyboard import Key, Controller

keyboard = Controller()

def coinSpender():
	bagOpen = False

	# Press alt first
	keyboard.press(Key.alt) # alt ne radi sa pyautogui
	time.sleep(random.uniform(0.1, 0.15))
	keyboard.release(Key.alt)
	time.sleep(random.uniform(0.2, 0.3))
	# After pressing alt once, do...
	while True:
		# Search of each potential image
		try:
			bag = pyautogui.locateCenterOnScreen('images/Inventory/Bag.jpg')
		except:
			bag = None 

		try:
			wealthButton = pyautogui.locateCenterOnScreen('images/Inventory/wealth.jpg')
		except:
			wealthButton = None

		try:
			activeWealthButton = pyautogui.locateOnScreen('images/Inventory/ActiveWealth.jpg')
		except:
			activeWealthButton = None

		try:
			spendButton = pyautogui.locateCenterOnScreen('images/Inventory/Spend.jpg')
		except:
			spendButton = None

		try:
			activeSpendButton = pyautogui.locateOnScreen('images/Inventory/ActiveSpend.jpg')
		except:
			activeSpendButton = None
		
		try:
			celestialSynergyButton = pyautogui.locateCenterOnScreen('images/Inventory/CelestialSynergy.jpg')
		except:
			celestialSynergyButton = None
		
		try:
			activeCelestialSynergyButton = pyautogui.locateOnScreen('images/Inventory/ActiveCelestialSynergy.jpg')
		except:
			activeCelestialSynergyButton = None
		
		try:
			celestialArtifactsButton = pyautogui.locateCenterOnScreen('images/Inventory/CelestialArtifacts.jpg')
		except:
			celestialArtifactsButton

		try:
			redeemButton = pyautogui.locateCenterOnScreen('images/Inventory/Redeem.jpg')
		except:
			redeemButton = None
		
		try:
			okButton = pyautogui.locateCenterOnScreen('images/Inventory/Ok.jpg')
		except:
			okButton = None
		
		try:
			activeOkButton = pyautogui.locateCenterOnScreen('images/Inventory/ActiveOk.jpg')
		except:
			activeOkButton = None

		if okButton:
			pyautogui.moveTo(okButton.x , okButton.y, random.uniform(0.3, 0.45))
			time.sleep(random.uniform(0.1, 0.2))
			while activeOkButton:
				try:
					activeOkButton = pyautogui.locateCenterOnScreen('images/Inventory/ActiveOk.jpg')
					pyautogui.click(activeOkButton)
					pyautogui.mouseUp(button='left')
				except:
					activeOkButton = None
			xButton = pyautogui.locateCenterOnScreen('images/Inventory/X.jpg')
			while xButton:
				try:
					xButton = pyautogui.locateCenterOnScreen('images/Inventory/X.jpg')
					time.sleep(random.uniform(0.3, 0.5))
					pyautogui.click(xButton)
					pyautogui.mouseUp(button='left')
				except:
					xButton = None
			break
		elif redeemButton:	
			moveAndInteract(redeemButton)
		elif celestialArtifactsButton:
			moveAndInteract(celestialArtifactsButton)
		elif celestialSynergyButton != None and activeCelestialSynergyButton == None:
			moveAndInteract(celestialSynergyButton)
		elif spendButton and activeSpendButton == None:
			bagOpen = True # Prebaciti u zaseban if
			moveAndInteract(spendButton)
		elif wealthButton and activeWealthButton == None:
			bagOpen = True # Prebaciti u zaseban if
			moveAndInteract(wealthButton)
		elif bag and bagOpen != True:
			moveAndInteract(bag)

def moveAndInteract(obj):
	pyautogui.moveTo(obj.x, obj.y, random.uniform(0.3, 0.45))
	pyautogui.click(obj)
	time.sleep(random.uniform(0.1, 0.2))
	pyautogui.mouseUp(button='left')
	time.sleep(random.uniform(0.2, 0.4))

def coinChecker():
	try:
		button11 = pyautogui.locateOnScreen('images\\Coins\\11-14.png')
	except:
		button11 = None
	try:
		button12 = pyautogui.locateOnScreen('images\\Coins\\12-14.jpg')
	except:
		button12 = None
	try:
		button13 = pyautogui.locateOnScreen('images\\Coins\\13-14.jpg')
	except:
		button13 = None
	try:
		button14 = pyautogui.locateOnScreen('images\\Coins\\14-14.jpg')
	except:
		button14 = None

	randomizer = random.choice([1, 2])
	# If less than 11 coins just continue
	if button11 == None and button12 == None and button13 == None and button14 == None:
		print('No enough coins')
	# If 14 coins spend 100% of time
	elif button14:
		coinSpender()
	# if 11, 12 or 13 coins spend 50% of time
	elif button11 or button12 or button13 and randomizer == 1:
		coinSpender()
	print("Done spending coins")
	return 0

coinChecker()

sys.stdout.flush()
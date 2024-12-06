const robot = require('robotjs');
const keypress = require('keypress');
const fs = require('fs');
const { resolve } = require('path');
const { rejects } = require('assert');
const { spawn } = require('child_process');
const colors = require('colors');


/* ============================================================= EDITABLE ====================================================================*/

// Total number of characters i.e. 9, 50, 36...
const charNumber = 21;

// Full path to log folder i.e. "C:/Program Files (x86)/Steam/steamapps/common/Cryptic Studios/Neverwinter/Live/logs/GameClient/" (CARE for quotation marks!)
const folderPath = `C:/Program Files (x86)/Steam/steamapps/common/Cryptic Studios/Neverwinter/Live/logs/GameClient/`;

// Monitor resolution (default: 1920x1080)
const MonitorResX = 1920;
const MonitorResY = 1080;

// Automatically spend Celestial Coins, true or false (default: true) 
const spendCoins = true;

// Invoke and logout keybind (default: f11)
const keybind = 'f11';

/* =========================================================================================================================================*/

/*Program intro*/

console.log(colors.red(`Welcome to NW invoke script \r\n`));
console.log(`> Your setup: \r\n - Number of characters: ${charNumber} \r\n - Path to log folder: ${folderPath} \r\n - Monitor resolution: ${MonitorResX}x${MonitorResY} \r\n - Spend Celestial Coins: ${spendCoins === true ? 'On' : 'Off'} \r\n - Keybind: ${keybind.charAt(0).toUpperCase()}${keybind.slice(1)} -> /bind ${keybind} "invoke $$ gotocharacterselect"\r\n`);
console.log('> Available commands:')
console.log(` - Start script: CTRL + F1 \r\n - Shutdown script: CTRL + C \r\n`);
console.log(colors.inverse(`> Before starting make sure you are in Character Select!`));

keypress(process.stdin);

// Key listener / Main process
process.stdin.on('keypress',  async (ch, key) => {
  // let mouse = robot.getMousePos();
  // console.log("Mouse is at x:" + mouse.x + " y:" + mouse.y);
  if (key) {
    switch(key.sequence) {
      // EXIT SCRIPT
      case '\x03':  // CTRL + C
        process.stdin.pause();
        break;
      // START SCRIPT
      case '\x1B[11^':  // CTRL + F1
        console.log(`Script started`);
        await minimizeScript();
        await scrollToBottom();
        await invoke();
        break;
      default:
        console.log(colors.red('> Unknown command!'));
        break;
    }
  } else {
    console.log(colors.red('> Unknown command!'));
  }
});

// Wait for certain time (in milliseconds)
const sleep = (waitTimeInMs) => new Promise(resolve => setTimeout(resolve, waitTimeInMs));
// Random number between min and max (decimal)
const randomInRange = (min, max) => Math.random() * (max - min) + min;


// Finds most recent file that matches today's log
const findMyFile = () => {
  const fullDate = new Date();
  const year = fullDate.getUTCFullYear();
  let month = fullDate.getUTCMonth() + 1;  // Starts from 0 so add 1
  month = ('0' + month).slice(-2);  // If less then 10 add 0 at start
  const day = fullDate.getUTCDate();
  
  const searchPattern = `voicechat_${year}-${month}-${day}`;
  const fileRegex = new RegExp(`^${searchPattern}`, 'i');
  // Array with all logs
  const logFolder =  fs.readdirSync(folderPath);
  // Array with logs that match searchPattern
  let listOfPotentialFiles = logFolder.filter(file => fileRegex.test(file));
  if (!listOfPotentialFiles[listOfPotentialFiles.length - 1]) {
    console.log('No logs found!');
    process.exit(1);
  }
  // Return last element from array (most recent log)
  return `${folderPath}${listOfPotentialFiles[listOfPotentialFiles.length - 1]}`;
};

const coinSpender = () => {
  const childPython = spawn('python', ['imageChecker.py']);
  return new Promise ((resolve, reject) => {
    childPython.stdout.on('data', data => {
      console.log(`${data}`);
      resolve(data);
    });
  });
};

// Watch log file and decide when to start or stop invoke
const watcherFunc = () => { 
  const lowKeybind = keybind.toLowerCase();
  const myFile = findMyFile();
  let logFileChangeCounter = 0;
  let logOutChecker = 0;
  return new Promise ((resolve, reject) => {
    const watcher = fs.watch(myFile, {persistent: false}, async (event, filename) => {
      if (filename && event == 'change') {
        logFileChangeCounter++;
        console.log(logFileChangeCounter);
        // Invoke when file change 2 times (every login)
        if (logFileChangeCounter === 2) {
          await sleep(randomInRange(400, 550));
          if (spendCoins === true) {
            await coinSpender();
            await sleep(randomInRange(300, 500));
          }
          robot.keyTap(lowKeybind);
          logOutChecker++;
        } 
        // End function when file changes ANOTHER 4 times (every log out) 
        else if (logFileChangeCounter >= 6) {
          await sleep(randomInRange(173, 257));
          // Escape ?anticheat?
          robot.keyTap('command');
          await sleep(randomInRange(100, 200));
          robot.keyTap('command');
          
          watcher.close();
          resolve(logFileChangeCounter);
        }
      }
    })
  })
};

// Log in, invoke, Log out
const inInvokeOut = async () => {
  await sleep(randomInRange(100, 200));
  robot.mouseClick('left', true); // Double left click
  await watcherFunc();
  await sleep(randomInRange(3000, 5000));
};

const minimizeScript = async () => {
  await sleep(200);
  robot.moveMouse(MonitorResX / 1.063711911357341, MonitorResY / 108);
  robot.mouseClick();
  console.log('Minimized Script!');
};

// Move to bottom of char select
const scrollToBottom = async () => { 
  robot.moveMouse(MonitorResX / 2.285714285714286, MonitorResY / 4.357142857142857);
  await sleep(500);
  let i = 0;
  // Moves character select to top
  while (i <= 5) {
    robot.mouseToggle('down', 'left');
    await sleep(100);
    robot.mouseToggle('up', 'left');
    i++;
  }
  await sleep(500);
  robot.mouseToggle('down');
  await sleep(100);
  robot.moveMouseSmooth(MonitorResX / 2.288438617401669, MonitorResY / 1.238532110091743);
  robot.mouseToggle('up');
  robot.moveMouse(MonitorResX / 3.127035830618893, MonitorResY / 1.285714285714286);
  console.log('Scrolled to the bottom of character select!');
};

// Invoke 1 full cycle
const invoke = async () => {
  let invokeCounter = 0;
  let yMax = MonitorResY / 1.489557083906465;
  let yMin = MonitorResY / 1.651376146788991;
  
  // Invokes until top of character select
  for (let i = 0; i < charNumber - 7; i++) {
    // For first invoke dont move mouse to 2nd from bottom position
    if (i != 0) {
      robot.moveMouse(randomInRange(MonitorResX / 4.528301886792453, MonitorResX / 2.330097087378641), randomInRange(MonitorResY / 1.473758903960045, MonitorResY /1.351689612015019));
    };
    await inInvokeOut();
    invokeCounter++
    console.log(`Completed invoke number ${invokeCounter}!`);
  };
  // Last 7 invokes
  for (let i = 0 ; i < 7; i++) {
    robot.moveMouse(randomInRange(MonitorResX / 4.528301886792453, MonitorResX / 2.330097087378641), randomInRange(yMin, yMax));
    await inInvokeOut();
    yMax -= MonitorResY / 13.25;
    yMin -= MonitorResY / 13.25;
    invokeCounter++
    console.log(`Completed invoke number ${invokeCounter}!`);
  };
};

process.stdin.setRawMode(true);
process.stdin.resume();

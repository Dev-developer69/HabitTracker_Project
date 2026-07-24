"""
Clock feature module for Habit Tracker (Streamlit).

Usage in your main app.py:

    from clock_feature import render_clock_section, render_home_countdown

    # Full clock widget (Clock / Stopwatch / Timer tabs) behind a button:
    if st.button("Clock"):
        st.session_state.show_clock = not st.session_state.get("show_clock", False)
    if st.session_state.get("show_clock", False):
        render_clock_section()

    # Small always-visible countdown box directly on the home page:
    render_home_countdown()
"""

import streamlit as st
import streamlit.components.v1 as components


def render_clock_section(height: int = 480):
    """Renders a tabbed Clock widget: Live Clock, Stopwatch, Countdown Timer.
    Pure JS/HTML — runs in-browser, no Streamlit reruns needed, so it ticks smoothly.
    Theme: black background, white text.
    """

    widget_html = """
    <div id="clock-widget" style="font-family: 'Segoe UI', sans-serif; max-width: 480px;">
      <style>
        #clock-widget * { box-sizing: border-box; }
        #clock-widget { background: #000; border-radius: 16px; padding: 16px; }
        .tabs { display: flex; gap: 8px; margin-bottom: 16px; }
        .tab-btn {
          flex: 1; padding: 10px; border: none; border-radius: 10px;
          background: #1a1a1a; color: #fff; font-weight: 600; cursor: pointer; font-size: 14px;
          border: 1px solid #333;
        }
        .tab-btn.active { background: #fff; color: #000; }
        .panel { display: none; text-align: center; padding: 20px;
                 border-radius: 14px; background: #111; }
        .panel.active { display: block; }
        .display { font-size: 42px; font-weight: 700; color: #fff; margin: 12px 0; }
        .controls { display: flex; gap: 10px; justify-content: center; margin-top: 10px; }
        .ctrl-btn { padding: 8px 18px; border: none; border-radius: 8px;
                    background: #fff; color: #000; font-weight: 600; cursor: pointer; }
        .ctrl-btn.stop { background: #e5534b; color: #fff; }
        .ctrl-btn.reset { background: #333; color: #fff; }
        input[type=number] { width: 70px; padding: 6px; border-radius: 6px;
                              border: 1px solid #444; background: #1a1a1a; color: #fff;
                              text-align: center; font-size: 16px; }
        #liveDate { color: #aaa; }
        #timerMsg { color: #ff6b6b; }
      </style>

      <div class="tabs">
        <button class="tab-btn active" onclick="showTab('clockTab', this)">🕐 Clock</button>
        <button class="tab-btn" onclick="showTab('stopwatchTab', this)">⏱️ Stopwatch</button>
        <button class="tab-btn" onclick="showTab('timerTab', this)">⏳ Timer</button>
      </div>

      <div id="clockTab" class="panel active">
        <div class="display" id="liveClock">--:--:--</div>
        <div id="liveDate"></div>
      </div>

      <div id="stopwatchTab" class="panel">
        <div class="display" id="swDisplay">00:00.00</div>
        <div class="controls">
          <button class="ctrl-btn" onclick="swStart()">Start</button>
          <button class="ctrl-btn stop" onclick="swStop()">Stop</button>
          <button class="ctrl-btn reset" onclick="swReset()">Reset</button>
        </div>
      </div>

      <div id="timerTab" class="panel">
        <div id="timerSetup">
          <input type="number" id="tMin" placeholder="min" min="0" value="5">
          :
          <input type="number" id="tSec" placeholder="sec" min="0" max="59" value="0">
        </div>
        <div class="display" id="timerDisplay">05:00</div>
        <div class="controls">
          <button class="ctrl-btn" onclick="timerStart()">Start</button>
          <button class="ctrl-btn stop" onclick="timerStop()">Stop</button>
          <button class="ctrl-btn reset" onclick="timerReset()">Reset</button>
        </div>
        <div id="timerMsg" style="margin-top:10px; font-weight:600;"></div>
      </div>
    </div>

    <script>
      function showTab(id, btn) {
        document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.getElementById(id).classList.add('active');
        btn.classList.add('active');
      }

      function updateClock() {
        const now = new Date();
        document.getElementById('liveClock').textContent = now.toLocaleTimeString();
        document.getElementById('liveDate').textContent = now.toDateString();
      }
      setInterval(updateClock, 1000);
      updateClock();

      let swInterval = null, swElapsed = 0, swStartTime = 0;
      function swTick() {
        const now = Date.now();
        const total = swElapsed + (now - swStartTime);
        const mins = String(Math.floor(total / 60000)).padStart(2, '0');
        const secs = String(Math.floor((total % 60000) / 1000)).padStart(2, '0');
        const cs = String(Math.floor((total % 1000) / 10)).padStart(2, '0');
        document.getElementById('swDisplay').textContent = `${mins}:${secs}.${cs}`;
      }
      function swStart() {
        if (swInterval) return;
        swStartTime = Date.now();
        swInterval = setInterval(swTick, 50);
      }
      function swStop() {
        if (!swInterval) return;
        swElapsed += Date.now() - swStartTime;
        clearInterval(swInterval);
        swInterval = null;
      }
      function swReset() {
        clearInterval(swInterval);
        swInterval = null;
        swElapsed = 0;
        document.getElementById('swDisplay').textContent = '00:00.00';
      }

      function playAlarm() {
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        let beeps = 0;
        function beep() {
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();
          osc.type = 'sine';
          osc.frequency.value = 880;
          gain.gain.setValueAtTime(0.3, ctx.currentTime);
          gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.4);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start();
          osc.stop(ctx.currentTime + 0.4);
          beeps++;
          if (beeps < 4) setTimeout(beep, 500);
        }
        beep();
      }

      let timerInterval = null, timerRemaining = 0;
      function timerFormat(sec) {
        const m = String(Math.floor(sec / 60)).padStart(2, '0');
        const s = String(sec % 60).padStart(2, '0');
        return `${m}:${s}`;
      }
      function timerReset() {
        clearInterval(timerInterval);
        timerInterval = null;
        document.getElementById('timerMsg').textContent = '';
        const min = parseInt(document.getElementById('tMin').value || 0);
        const sec = parseInt(document.getElementById('tSec').value || 0);
        timerRemaining = min * 60 + sec;
        document.getElementById('timerDisplay').textContent = timerFormat(timerRemaining);
      }
      function timerStart() {
        if (timerInterval) return;
        if (timerRemaining <= 0) {
          const min = parseInt(document.getElementById('tMin').value || 0);
          const sec = parseInt(document.getElementById('tSec').value || 0);
          timerRemaining = min * 60 + sec;
        }
        timerInterval = setInterval(() => {
          timerRemaining--;
          document.getElementById('timerDisplay').textContent = timerFormat(Math.max(timerRemaining, 0));
          if (timerRemaining <= 0) {
            clearInterval(timerInterval);
            timerInterval = null;
            document.getElementById('timerMsg').textContent = "⏰ Time's up!";
            playAlarm();
          }
        }, 1000);
      }
      function timerStop() {
        clearInterval(timerInterval);
        timerInterval = null;
      }
      timerReset();
    </script>
    """

    components.html(widget_html, height=height, scrolling=False)


def render_home_countdown(height: int = 160):
    """A small, always-visible countdown box for the home page.
    Black background, white text. Independent of render_clock_section."""

    widget_html = """
    <div id="home-cd" style="font-family: 'Segoe UI', sans-serif; max-width: 320px;
         background:#000; color:#fff; border-radius: 14px; padding: 16px; text-align:center;">
      <style>
        #home-cd input[type=number] {
          width: 55px; padding: 5px; border-radius: 6px; border: 1px solid #444;
          background: #1a1a1a; color: #fff; text-align: center; font-size: 14px;
        }
        #home-cd .cd-display { font-size: 30px; font-weight: 700; margin: 8px 0; }
        #home-cd button {
          padding: 6px 14px; border: none; border-radius: 8px; font-weight: 600;
          cursor: pointer; margin: 0 3px; background: #fff; color: #000;
        }
        #home-cd button.stop { background:#e5534b; color:#fff; }
        #home-cd button.reset { background:#333; color:#fff; }
        #home-cd .cd-msg { color:#ff6b6b; font-weight:600; margin-top:6px; min-height:18px; }
      </style>
      <div style="font-size:13px; color:#aaa; margin-bottom:6px;">⏳ Quick Countdown</div>
      <div>
        <input type="number" id="hcMin" min="0" value="5"> :
        <input type="number" id="hcSec" min="0" max="59" value="0">
      </div>
      <div class="cd-display" id="hcDisplay">05:00</div>
      <div>
        <button onclick="hcStart()">Start</button>
        <button class="stop" onclick="hcStop()">Stop</button>
        <button class="reset" onclick="hcReset()">Reset</button>
      </div>
      <div class="cd-msg" id="hcMsg"></div>
    </div>

    <script>
      let hcInterval = null, hcRemaining = 0;
      function hcFormat(sec) {
        const m = String(Math.floor(sec / 60)).padStart(2, '0');
        const s = String(sec % 60).padStart(2, '0');
        return `${m}:${s}`;
      }
      function hcPlayAlarm() {
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        let beeps = 0;
        function beep() {
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();
          osc.type = 'sine';
          osc.frequency.value = 880;
          gain.gain.setValueAtTime(0.3, ctx.currentTime);
          gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.4);
          osc.connect(gain); gain.connect(ctx.destination);
          osc.start(); osc.stop(ctx.currentTime + 0.4);
          beeps++;
          if (beeps < 4) setTimeout(beep, 500);
        }
        beep();
      }
      function hcReset() {
        clearInterval(hcInterval); hcInterval = null;
        document.getElementById('hcMsg').textContent = '';
        const min = parseInt(document.getElementById('hcMin').value || 0);
        const sec = parseInt(document.getElementById('hcSec').value || 0);
        hcRemaining = min * 60 + sec;
        document.getElementById('hcDisplay').textContent = hcFormat(hcRemaining);
      }
      function hcStart() {
        if (hcInterval) return;
        if (hcRemaining <= 0) {
          const min = parseInt(document.getElementById('hcMin').value || 0);
          const sec = parseInt(document.getElementById('hcSec').value || 0);
          hcRemaining = min * 60 + sec;
        }
        hcInterval = setInterval(() => {
          hcRemaining--;
          document.getElementById('hcDisplay').textContent = hcFormat(Math.max(hcRemaining, 0));
          if (hcRemaining <= 0) {
            clearInterval(hcInterval); hcInterval = null;
            document.getElementById('hcMsg').textContent = "Time's up!";
            hcPlayAlarm();
          }
        }, 1000);
      }
      function hcStop() { clearInterval(hcInterval); hcInterval = null; }
      hcReset();
    </script>
    """

    components.html(widget_html, height=height, scrolling=False)

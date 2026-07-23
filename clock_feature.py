"""
Clock feature module for Habit Tracker (Streamlit).

Usage in your main app.py:

    from clock_feature import render_clock_section
    ...
    if st.button("⏱️ Clock"):
        st.session_state.show_clock = not st.session_state.get("show_clock", False)

    if st.session_state.get("show_clock", False):
        render_clock_section()
"""

import streamlit as st
import streamlit.components.v1 as components


def render_clock_section(height: int = 480):
    """Renders a tabbed Clock widget: Live Clock, Stopwatch, Countdown Timer.
    Pure JS/HTML — runs in-browser, no Streamlit reruns needed, so it ticks smoothly.
    """

    widget_html = """
    <div id="clock-widget" style="font-family: 'Segoe UI', sans-serif; max-width: 480px;">
      <style>
        #clock-widget * { box-sizing: border-box; }
        .tabs { display: flex; gap: 8px; margin-bottom: 16px; }
        .tab-btn {
          flex: 1; padding: 10px; border: none; border-radius: 10px;
          background: linear-gradient(135deg, #a8d5ba, #b8a8d5);
          color: #333; font-weight: 600; cursor: pointer; font-size: 14px;
        }
        .tab-btn.active { background: #2f2f2f; color: white; }
        .panel { display: none; text-align: center; padding: 20px;
                 border-radius: 14px; background: #f4f7f5; }
        .panel.active { display: block; }
        .display { font-size: 42px; font-weight: 700; color: #444; margin: 12px 0; }
        .controls { display: flex; gap: 10px; justify-content: center; margin-top: 10px; }
        .ctrl-btn { padding: 8px 18px; border: none; border-radius: 8px;
                    background: #a8d5ba; font-weight: 600; cursor: pointer; }
        .ctrl-btn.stop { background: #e5a3a3; }
        .ctrl-btn.reset { background: #ddd; }
        input[type=number] { width: 70px; padding: 6px; border-radius: 6px;
                              border: 1px solid #ccc; text-align: center; font-size: 16px; }
      </style>

      <div class="tabs">
        <button class="tab-btn active" onclick="showTab('clockTab', this)">🕐 Clock</button>
        <button class="tab-btn" onclick="showTab('stopwatchTab', this)">⏱️ Stopwatch</button>
        <button class="tab-btn" onclick="showTab('timerTab', this)">⏳ Timer</button>
      </div>

      <div id="clockTab" class="panel active">
        <div class="display" id="liveClock">--:--:--</div>
        <div id="liveDate" style="color:#777;"></div>
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
        <div id="timerMsg" style="margin-top:10px; font-weight:600; color:#c0392b;"></div>
      </div>
    </div>

    <script>
      function showTab(id, btn) {
        document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.getElementById(id).classList.add('active');
        btn.classList.add('active');
      }

      // Live clock
      function updateClock() {
        const now = new Date();
        document.getElementById('liveClock').textContent = now.toLocaleTimeString();
        document.getElementById('liveDate').textContent = now.toDateString();
      }
      setInterval(updateClock, 1000);
      updateClock();

      // Stopwatch
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

      // Alarm sound (Web Audio API — no external file needed)
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

      // Countdown timer
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
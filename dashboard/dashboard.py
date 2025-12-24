# dashboard.py
from flask import Flask, render_template_string, Response
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime

app = Flask(__name__)

# Store detection events
alerts = []

# Count detections
stats = {
    'normal': 0,
    'attack': 0
}

# Home page
@app.route('/')
def index():
    # Create pie chart
    fig, ax = plt.subplots(figsize=(6, 4))
    labels = ['Normal', 'Attack']
    values = [stats['normal'], stats['attack']]
    colors = ['#2ecc71', '#e74c3c']
    
    if sum(values) == 0:
        values = [1, 1]  # Show equal if no data
        labels = ['', '']
        ax.pie(values, labels=labels, colors=['#cccccc', '#cccccc'], textprops={'color': 'w'})
        plt.legend(labels=['No data yet'], loc='center')
    else:
        ax.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', textprops={'color': 'white'})

    plt.title("Traffic Detection Summary", color='#2c3e50')

    # Save plot to bytes
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', facecolor='#f8f9fa')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    html = f'''
    <html>
        <head>
            <title>IoT Security Dashboard</title>
            <meta http-equiv="refresh" content="2">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f8f9fa; }}
                h1 {{ color: #2c3e50; }}
                .alert {{ padding: 10px; margin: 10px 0; border-radius: 5px; }}
                .normal {{ background-color: #dffeef; border-left: 5px solid #2ecc71; }}
                .attack {{ background-color: #ffeded; border-left: 5px solid #e74c3c; }}
                .timestamp {{ color: #7f8c8d; font-size: 0.9em; }}
                .graph {{ text-align: center; margin: 20px 0; }}
                img {{ border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
            </style>
        </head>
        <body>
            <h1>🛡️ IoT Security Dashboard</h1>
            <p><strong>Last updated:</strong> {datetime.now().strftime('%H:%M:%S')}</p>

            <div class="graph">
                <img src="data:image/png;base64,{plot_url}" alt="Detection Chart">
            </div>

            <div id="alerts">
                {{% if alerts %}}
                  {{% for alert in alerts %}}
                    <div class="alert {{{{ alert['type'] }}}}">
                        <strong>{{{{ alert['device'] }}}}</strong><br>
                        IP: {{{{ alert['ip'] }}}} | Type: {{{{ alert['atype'] }}}}<br>
                        <span class="timestamp">{{{{ alert['time'] }}}}</span>
                    </div>
                  {{% endfor %}}
                {{% else %}}
                  <p>No threats detected.</p>
                {{% endif %}}
            </div>
        </body>
    </html>
    '''
    return render_template_string(html, alerts=alerts)

# Route to add normal device
@app.route('/normal/<ip>/<name>')
def add_normal(ip, name):
    global alerts, stats
    alerts.append({
        'device': f"🟢 {name}",
        'ip': ip,
        'atype': 'Normal Traffic',
        'type': 'normal',
        'time': datetime.now().strftime('%H:%M:%S')
    })
    stats['normal'] += 1
    return "OK", 200

# Route to add attack
@app.route('/attack/<ip>/<atype>')
def add_attack(ip, atype):
    global alerts, stats
    alerts.append({
        'device': f"🔴 MALICIOUS DEVICE",
        'ip': ip,
        'atype': atype,
        'type': 'attack',
        'time': datetime.now().strftime('%H:%M:%S')
    })
    stats['attack'] += 1
    return "OK", 200

if __name__ == '__main__':
    import threading
    import time

    def run_flask():
        app.run(port=5000, debug=False, use_reloader=False)

    # Start Flask in background thread
    threading.Thread(target=run_flask, daemon=True).start()

    print("🌍 Dashboard started at http://localhost:5000")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped.")

import psutil
import webbrowser
import subprocess

class CommandExecutor:
    @staticmethod
    def process_command(cmd: str) -> str:
        cmd = cmd.lower().strip()
        
        # 1. System Telemetry
        if "cpu usage" in cmd:
            return f"CPU load is currently at {psutil.cpu_percent()}%"
        elif "ram usage" in cmd:
            return f"Memory utilization is at {psutil.virtual_memory().percent}%"
            
        # 2. Dynamic "Open" Command Routing
        if cmd.startswith("open "):
            target = cmd.replace("open ", "").strip()
            
            # Dictionary of common web portals
            websites = {
                "youtube": "https://youtube.com",
                "linkedin": "https://linkedin.com",
                "github": "https://github.com",
                "gmail": "https://mail.google.com",
                "google": "https://google.com",
                "wikipedia": "https://wikipedia.org",
                "whatsapp": "https://web.whatsapp.com"
            }
            
            # Route A: It's a known website
            if target in websites:
                webbrowser.open(websites[target])
                return f"Accessing {target.title()} web portal."
            
            # Route B: It's a local macOS App (Chrome, VS Code, Spotify, etc.)
            try:
                # macOS 'open -a' command launches applications natively
                # stderr=subprocess.DEVNULL hides error text if the app doesn't exist
                subprocess.run(["open", "-a", target], check=True, stderr=subprocess.DEVNULL)
                return f"Launching the {target.title()} application."
            except subprocess.CalledProcessError:
                # If the app doesn't exist, return empty string so the LLM can try to answer it
                return ""
        
        return ""

executor = CommandExecutor()
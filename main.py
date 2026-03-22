import customtkinter
import urllib.parse
import subprocess
import threading

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Video Downloader Pro")
        self.geometry("500x300")
        
        self.grid_columnconfigure(0, weight=1)

        self.title_label = customtkinter.CTkLabel(self, text="YouTube Downloader", font=("Roboto", 24, "bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.url_entry = customtkinter.CTkEntry(self, placeholder_text="Paste YouTube URL here", width=400, height=40)
        self.url_entry.grid(row=1, column=0, padx=20, pady=10)

        self.download_btn = customtkinter.CTkButton(self, text="Download Video", command=self.start_download_thread, fg_color="#1f6aa5", hover_color="#144870")
        self.download_btn.grid(row=2, column=0, padx=20, pady=10)

        self.status_label = customtkinter.CTkLabel(self, text="", font=("Roboto", 12))
        self.status_label.grid(row=3, column=0, padx=20, pady=5)

        self.progress_bar = customtkinter.CTkProgressBar(self, width=400)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=4, column=0, padx=20, pady=10)

    def update_status(self, text, color="white"):
        self.status_label.configure(text=text, text_color=color)

    def start_download_thread(self):
        video_url = self.url_entry.get()
        
        parsed_url = urllib.parse.urlparse(video_url)
        if not video_url:
            self.update_status("Please insert a URL!", "red")
            return
            
        if "youtube.com" not in parsed_url.netloc and "youtu.be" not in parsed_url.netloc:
            self.update_status("Invalid URL for YouTube.", "red")
            return

        self.download_btn.configure(state="disabled")
        self.progress_bar.start()
        
        thread = threading.Thread(target=self.download_logic, args=(video_url,))
        thread.start()

    def download_logic(self, video_url):
        try:
            self.update_status("Download in progress...", "yellow")
            subprocess.run([
                "yt-dlp",
                "-f", "bv*+ba/b",
                "--retries", "infinite",
                "--fragment-retries", "infinite",
                "--retry-sleep", "fragment:5",
                "--concurrent-fragments", "1",
                "--merge-output-format", "mp4",
                "-o", "input.%(ext)s",
                video_url
            ])
            
            import time
            time.sleep(3) 

            self.update_status("Download completed successfully!", "green")
        except Exception as e:
            self.update_status(f"Error: {str(e)}", "red")
        finally:
            self.download_btn.configure(state="normal")
            self.progress_bar.stop()
            self.progress_bar.set(1)

if __name__ == "__main__":
    app = App()
    app.mainloop()




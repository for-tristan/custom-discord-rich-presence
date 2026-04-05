import customtkinter as ctk
from pypresence import Presence
import threading
import time

ctk.set_appearance_mode("dark")

BG_COLOR = "#111214"
CARD_COLOR = "#111214"
INPUT_BG = "#111214"
TEXT_COLOR = "#f2f3f5"
SUBTEXT_COLOR = "#fcfcfc"
ACCENT_COLOR = "#5865f2"
GREEN_COLOR = "#3ac065"
RED_COLOR = "#b42f31"
YELLOW_COLOR = "#d3bd42"

class ModernRPCApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.configure(fg_color=BG_COLOR)
        self.title("Discord RPC")
        self.geometry("500x680")
        self.resizable(False, False)

        self.rpc = None
        self.is_running = False
        self.start_time = int(time.time())
        self.animation_state = False

        self.setup_ui()

    def setup_ui(self):
        header = ctk.CTkFrame(self, fg_color="transparent", height=70)
        header.pack(fill="x", padx=30, pady=(35, 15))
        header.pack_propagate(False)

        ctk.CTkLabel(header, text="Discord Rich Presence", font=ctk.CTkFont(family="Helvetica", size=26, weight="bold"), text_color=TEXT_COLOR).pack(side="left")

        self.status_canvas = ctk.CTkCanvas(header, width=20, height=20, bg=BG_COLOR, highlightthickness=0)
        self.status_canvas.pack(side="right", pady=25)
        self.draw_status_dot("#4e5058")

        self.status_text = ctk.CTkLabel(header, text="idle", font=ctk.CTkFont("Helvetica", size=14), text_color=SUBTEXT_COLOR)
        self.status_text.pack(side="right", padx=(0, 8))

        conn_card = ctk.CTkFrame(self, fg_color=CARD_COLOR, corner_radius=8)
        conn_card.pack(fill="x", padx=30, pady=(0, 15))

        ctk.CTkLabel(conn_card, text="CONNECTION", font=ctk.CTkFont("Helvetica", size=11, weight="bold", slant="italic"), text_color=SUBTEXT_COLOR).pack(anchor="w", padx=20, pady=(20, 8))

        self.app_id_entry = ctk.CTkEntry(conn_card, placeholder_text="Discord Application ID", fg_color=INPUT_BG, border_width=1, text_color=TEXT_COLOR, height=45)
        self.app_id_entry.pack(fill="x", padx=20, pady=(0, 20))

        self.test_btn = ctk.CTkButton(
            conn_card, fg_color="transparent", border_width=1, border_color=ACCENT_COLOR, hover_color="#4752c4",
            height=40, text="Test Connection", font=ctk.CTkFont("Helvetica"), text_color=ACCENT_COLOR,
            command=self.test_connection_thread
        )
        self.test_btn.pack(fill="x", padx=20, pady=(0, 20))

        status_card = ctk.CTkFrame(self, fg_color=CARD_COLOR, corner_radius=8)
        status_card.pack(fill="x", padx=30, pady=(0, 20))

        ctk.CTkLabel(status_card, text="PRESENCE DETAILS", font=ctk.CTkFont("Helvetica", size=11, weight="bold", slant="italic"), text_color=SUBTEXT_COLOR).pack(anchor="w", padx=20, pady=(20, 8))

        self.details_entry = ctk.CTkEntry(status_card, placeholder_text="Details", fg_color=INPUT_BG, border_width=1, text_color=TEXT_COLOR, height=45)
        self.details_entry.pack(fill="x", padx=20, pady=(0, 12))

        self.state_entry = ctk.CTkEntry(status_card, placeholder_text="State", fg_color=INPUT_BG, border_width=1, text_color=TEXT_COLOR, height=45)
        self.state_entry.pack(fill="x", padx=20, pady=(0, 12))

        self.image_entry = ctk.CTkEntry(status_card, placeholder_text="Image Key (Optional)", fg_color=INPUT_BG, border_width=1, text_color=TEXT_COLOR, height=45)
        self.image_entry.pack(fill="x", padx=20, pady=(0, 20))

        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.pack(fill="x", padx=30, pady=(0, 15))

        self.start_btn = ctk.CTkButton(action_frame, text="Start", fg_color=GREEN_COLOR, hover_color="#3ba55d", text_color="#111214", font=ctk.CTkFont("Helvetica", weight="bold", size=13), height=48, corner_radius=8, command=self.start_rpc)
        self.start_btn.pack(side="left", expand=True, fill="x", padx=(0, 8))

        self.stop_btn = ctk.CTkButton(action_frame, text="Stop", fg_color=RED_COLOR, hover_color="#c0353a", text_color="#111214", font=ctk.CTkFont("Helvetica", weight="bold", size=13), height=48, corner_radius=8, state="disabled", command=self.stop_rpc)
        self.stop_btn.pack(side="right", expand=True, fill="x", padx=(8, 0))

        self.update_btn = ctk.CTkButton(self, text="Apply Changes", fg_color=ACCENT_COLOR, hover_color="#4752c4", text_color="#ffffff", font=ctk.CTkFont("Helvetica", weight="bold", size=13), height=45, corner_radius=8, state="disabled", command=self.live_update)
        self.update_btn.pack(fill="x", padx=30, pady=(0, 20))

        self.toggle_inputs(False)

    def draw_status_dot(self, color, size=6):
        self.status_canvas.delete("all")
        self.status_canvas.create_oval(10 - size, 10 - size, 10 + size, 10 + size, fill=color, outline="")

    def animate_status(self):
        if not self.animation_state:
            return
        next_size = 8 if int(time.time() * 2) % 2 == 0 else 6
        self.draw_status_dot(GREEN_COLOR, next_size)
        self.after(400, self.animate_status)

    def set_ui_state(self, connected):
        self.is_running = connected
        self.start_btn.configure(state="disabled" if connected else "normal")
        self.stop_btn.configure(state="normal" if connected else "disabled")
        self.update_btn.configure(state="normal" if connected else "disabled")
        self.app_id_entry.configure(state="disabled" if connected else "normal")
        self.test_btn.configure(state="disabled" if connected else "normal")
        self.toggle_inputs(connected)

        if connected:
            self.animation_state = True
            self.status_text.configure(text="Active", text_color=GREEN_COLOR)
            self.animate_status()
        else:
            self.animation_state = False
            self.draw_status_dot("#4e5058", 6)
            self.status_text.configure(text="Idle", text_color=SUBTEXT_COLOR)

    def toggle_inputs(self, enabled):
        state = "normal" if enabled else "disabled"
        self.details_entry.configure(state=state)
        self.state_entry.configure(state=state)
        self.image_entry.configure(state=state)

    def test_connection_thread(self):
        app_id = self.app_id_entry.get().strip()
        if not app_id:
            self.status_text.configure(text="No ID!", text_color=RED_COLOR)
            self.draw_status_dot(RED_COLOR, 6)
            return

        self.test_btn.configure(state="disabled", text="Testing...")
        self.status_text.configure(text="Testing...", text_color=YELLOW_COLOR)
        self.draw_status_dot(YELLOW_COLOR, 6)
        threading.Thread(target=self._test_connection, args=(app_id,), daemon=True).start()

    def _test_connection(self, app_id):
        test_rpc = None
        try:
            test_rpc = Presence(app_id)
            test_rpc.connect()
            self.after(0, self._test_success)
        except Exception as e:
            err_msg = "Failed"
            if "ConnectionError" in str(type(e).__name__):
                err_msg = "App Closed"
            elif "InvalidID" in str(e):
                err_msg = "Bad ID"
            self.after(0, self._test_fail, err_msg)
        finally:
            if test_rpc:
                try:
                    test_rpc.close()
                except:
                    pass

    def _test_success(self):
        self.test_btn.configure(state="normal", text="Test Connection")
        self.status_text.configure(text="Connected!", text_color=GREEN_COLOR)
        self.draw_status_dot(GREEN_COLOR, 6)

    def _test_fail(self, msg):
        self.test_btn.configure(state="normal", text="Test Connection")
        self.status_text.configure(text=msg, text_color=RED_COLOR)
        self.draw_status_dot(RED_COLOR, 6)

    def start_rpc(self):
        app_id = self.app_id_entry.get().strip()
        if not app_id:
            return

        try:
            self.rpc = Presence(app_id)
            self.rpc.connect()
            self.start_time = int(time.time())

            details = self.details_entry.get().strip() or "None"
            state = self.state_entry.get().strip() or "None"
            image = self.image_entry.get().strip() or None

            self.rpc.update(details=details, state=state, large_image=image, start=self.start_time)
            self.set_ui_state(True)
        except Exception as e:
            self.status_text.configure(text="Error", text_color=RED_COLOR)
            self.draw_status_dot(RED_COLOR, 6)

    def live_update(self):
        if not self.is_running or not self.rpc:
            return
        try:
            details = self.details_entry.get().strip() or "None"
            state = self.state_entry.get().strip() or "None"
            image = self.image_entry.get().strip() or None

            self.rpc.update(details=details, state=state, large_image=image, start=self.start_time)
            self.status_text.configure(text="Updated!", text_color=ACCENT_COLOR)
            self.after(1500, lambda: self.status_text.configure(text="Active", text_color=GREEN_COLOR))
        except:
            self.status_text.configure(text="Update Err", text_color=RED_COLOR)

    def stop_rpc(self):
        if self.rpc:
            try:
                self.rpc.clear()
                self.rpc.close()
            except:
                pass
        self.set_ui_state(False)

if __name__ == "__main__":
    app = ModernRPCApp()
    app.update_idletasks()
    x = (app.winfo_screenwidth() // 2) - (500 // 2)
    y = (app.winfo_screenheight() // 2) - (680 // 2)
    app.geometry(f"500x680+{x}+{y}")
    app.mainloop()
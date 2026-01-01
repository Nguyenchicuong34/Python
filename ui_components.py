import customtkinter as ctk

class InfoCard(ctk.CTkFrame):
    def __init__(self, master, title, content, sub_info, action_name=None, action_cmd=None, **kwargs):
        super().__init__(master, fg_color="#333333", corner_radius=10, **kwargs)
        
        self.pack(fill="x", pady=5, padx=5)
        
      
        ctk.CTkLabel(self, text=title, font=("Arial", 14, "bold"), text_color="#4da6ff").pack(anchor="w", padx=10, pady=(10,0))
        
      
        ctk.CTkLabel(self, text=content, font=("Arial", 12), wraplength=400, justify="left").pack(anchor="w", padx=10, pady=2)
        
      
        ctk.CTkLabel(self, text=sub_info, font=("Arial", 10, "italic"), text_color="gray").pack(anchor="w", padx=10, pady=(0,10))

        
        if action_name and action_cmd:
            ctk.CTkButton(self, text=action_name, height=25, width=80, fg_color="#cc0000", command=action_cmd).pack(anchor="e", padx=10, pady=5)
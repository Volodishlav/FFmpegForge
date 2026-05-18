def arg_extensions():
    if args.extensions is not None:
        try:
            for ext in EXTENSIONS:
                if not ext.startswith("."):
                    raise ValueError(f"Invalid extension: {ext}")
                
            return {ext.strip().lower() for ext in args.extensions.split(",")}

        except Exception as e:
            print("Error:", e)

def arg_input():
    if args.input is not None:
        return args.input
    
def arg_output():
    if args.output is not None:
        return args.output
    
def arg_extensions_type():
    if args.image_extensions:
        return {".jpg", ".jpeg", ".png", ".webp", ".gif"}

    if args.video_extensions:
        return {".mp4", ".mkv", ".avi", ".mov", ".webm"}
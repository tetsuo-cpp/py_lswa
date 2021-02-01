import loader, scanner, updater
import threading


# Load initial data.
loader.load()

# threads = list()
# threads.append(threading.Thread(target=scanner.scan))
# threads.append(threading.Thread(target=updater.update))

scanner.scan()

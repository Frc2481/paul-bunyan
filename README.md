# paul-bunyan

## Dependancies
```
opkg update
opkg install python-pip
opkg install python-setuptools
opkg install python-opencv
```

### Network Tables 3.1
```
pip install https://pypi.python.org/packages/source/p/pynetworktables/pynetworktables-2015.3.1.tar.gz
```

## Installation
```
cd paul-bunyan
mv Camera.service /lib/systemd/system/
mv BirdWatcher.service /lib/systemd/system/
mv Camera ../Camera
mv Bird-Watcher ../Bird-Watcher
```

## Enable Services
```
systemctl enable Camera
systemctl enable BirdWatcher
```

## Static IP
```
ls -la /var/lib/connman/
cd /var/lib/connman/ethernet_[xx]
more settings
cd /usr/lib/connman/test
./set-ipv4-method ethernet_[xx]_cable manual 10.24.81.8 255.255.255.0 10.24.81.4
```

## View Log
```
journalctl --no-pager | grep python
```

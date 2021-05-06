# Installation

Installing this library is as easy as pip install!

```bash
pip install wyzecam
```

... almost. You will also need a copy of the shared library `libIOTCAPIs_ALL.so`. You will need
to [download this SDK](https://github.com/nblavoie/wyzecam-api/tree/master/wyzecam-sdk), unzip it, then convert the
appropriate copy of the library to a shared library, and copy the resultant `.so` or `.dylib` file to somewhere
convenient.

### On Mac:

```shell
unzip TUTK_IOTC_Platform_14W42P1.zip
cd Lib/MAC/
g++ -fpic -shared -Wl,-all_load libIOTCAPIs_ALL.a -o libIOTCAPIs_ALL.dylib
cp libIOTCAPIs_ALL.dylib /usr/local/lib/
```

### On Linux:

```bash
unzip TUTK_IOTC_Platform_14W42P1.zip
cd Lib/Linux/x64/
g++ -fpic -shared -Wl,-whole-archive libAVAPIs.a libIOTCAPIs.a -o libIOTCAPIs_ALL.so
cp libIOTCAPIs_ALL.so /usr/local/lib/
```

Note: you will need to pick the appropriate architecture.

### On Windows:

TBD (don't have a windows box handy, if anyone wants to test windows support, feel free to make a pull request!).

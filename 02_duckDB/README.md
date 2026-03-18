# Creating Virtual Environment
```bash 
$ python -m venv env
$ source env/bin/activate
(env) $ pip install --upgrade pip setuptools
(env) $ pip install -r requirements.txt
```
# Test
```bash
(env) $ python sample1_DBpath.py
(env) $ python sample2_memory.py
```

# Deactivate Virtual Environment
```bash
(env) $ deactivate
```

# Clean up
```bash
$ sudo rm -r env
```
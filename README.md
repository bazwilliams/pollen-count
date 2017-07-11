# Pollen Count

The skill and lambda backend for the Pollen Count Alexa Skill. 

## Development

```bash
python3 -m venv env
pip install pytest
pip install mock
```

```bash
pip install -r requirements.txt
```

## Testing

```bash
pytest ./tests
```

## Packaging

```bash
./package.hs
```

## Deploying

```bash
LAMBDA_TAG=n ./deploy.sh
```

## Credits

https://github.com/kylegordon/pypollen

Icon downloaded from https://www.iconfinder.com/icons/1320036/badge_go_pin_pokemon_sunflower_icon

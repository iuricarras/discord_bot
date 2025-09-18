{
  lib,
  python313Packages,
  ...
}:
python313Packages.buildPythonApplication {
  pname = "discordBot";
  version = "0.1.1";
  pyproject = true;

  build-system = [python313Packages.setuptools];

  propagatedBuildInputs = with python313Packages; [
    discordpy
    aiohttp
    unidecode
    yt-dlp
    pyradios
    python-dotenv
  ];
  checkInputs = with python313Packages; [
    discordpy
    aiohttp
    unidecode
    yt-dlp
    pyradios
    python-dotenv
  ];
  nativeBuildInputs = [python313Packages.setuptools python313Packages.pip];

  buildInputs = [
    python313Packages.setuptools
  ];

  src = ./.;

  meta = {
    description = "A simple Discord bot built with discord.py";
    homepage = "https://github.com/iuricarras/discord_bot";
    license = lib.licenses.mit;
  };
}

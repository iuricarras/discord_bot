{pkgs ? import <nixpkgs> {}}:
pkgs.mkShell {
  buildInputs = with pkgs; [
    python312
    python312Packages.discordpy
    python312Packages.aiohttp
    python312Packages.unidecode
    python312Packages.yt-dlp
    python312Packages.pyradios
    python312Packages.python-dotenv
  ];
}

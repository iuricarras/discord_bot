{pkgs ? import <nixpkgs> {}}:
let
  discordpyWithVoice = pkgs.python313Packages.discordpy.override { withVoice = true; };
in
pkgs.mkShell {
  buildInputs = with pkgs; [
    python313
    discordpyWithVoice
    python313Packages.aiohttp
    python313Packages.unidecode
    python313Packages.yt-dlp
    python313Packages.pyradios
    python313Packages.python-dotenv
    python313Packages.python-ffmpeg
    python313Packages.async-timeout
    python313Packages.pynacl
  ];
}

# PPVviaVLC

PPVviaVLC enables anyone to broadcast pay-per-view (PPV) live streams from the comfort of their own device using VLC. It tokenizes access to your encrypted VLC stream so viewers must purchase a token to watch. This repository now includes a Solidity smart contract for managing tokenized access.

## Features
- Uses standard VLC tools to stream directly from your machine.
- Token-based access allows you to charge per viewer.
- Keeps streams encrypted until a valid token is provided.

## Getting Started
1. Install VLC on your computer.
2. Clone this repository and configure the stream settings.
3. Launch your broadcast using VLC.
4. Share your tokens so viewers can watch the live PPV stream.
5. Windows users can run ppv_vlc_setup.py to automatically install or update VLC.

Remember to only stream content you have rights to share and comply with all local laws regarding pay-per-view broadcasts.

## Smart Contracts

The `contracts/BlockGroup1155.sol` file implements an ERC1155 token where token IDs are arranged in blocks of 64. Each block is managed by a user group. Token ID 0 is unlimited and acts as currency while IDs 1-63 are semi-fungible with supply caps set when the group is created. Payments for a group are split among actors using OpenZeppelin's `PaymentSplitter`.

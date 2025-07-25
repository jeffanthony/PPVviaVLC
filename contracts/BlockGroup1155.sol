// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/finance/PaymentSplitter.sol";

/**
 * @title BlockGroup1155
 * @dev ERC1155 contract where token IDs are grouped in blocks of 64. Each group
 *      has associated roles for managing streams and payments. Payments can be
 *      split among actors using OpenZeppelin's PaymentSplitter.
 */
contract BlockGroup1155 is ERC1155, AccessControl {
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");

    // tokenId => maximum supply (0 means unlimited)
    mapping(uint256 => uint256) private _maxSupply;
    // tokenId => minted amount
    mapping(uint256 => uint256) private _minted;

    /// @dev Returns the configured max supply for a token id (0 if unlimited)
    function maxSupply(uint256 id) external view returns (uint256) {
        return _maxSupply[id];
    }

    /// @dev Returns the number of tokens minted so far for a token id
    function minted(uint256 id) external view returns (uint256) {
        return _minted[id];
    }

    struct UserGroup {
        address paymentSplitter; // contract splitting payments between actors
        address chatModerator;   // moderator address
        address techDev;         // technical support
        bool exists;             // flag to check if group is set
    }

    // mapping from group id => UserGroup
    mapping(uint256 => UserGroup) private userGroups;

    event GroupCreated(
        uint256 indexed groupId,
        address splitter,
        address chatModerator,
        address techDev
    );

    constructor(string memory uri) ERC1155(uri) {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(ADMIN_ROLE, msg.sender);
    }

    /**
     * @dev Returns the group id for a given token id
     */
    function groupIdForToken(uint256 tokenId) public pure returns (uint256) {
        return tokenId / 64; // integer division groups every 64 tokens
    }

    /**
     * @dev Create a user group for a block of 64 token IDs. Only admins may call.
     * @param groupId The id of the group (tokenId / 64)
     * @param payees Addresses to receive payments
     * @param shares Shares for each payee corresponding by index
     * @param chatModerator Address of chat moderator
     * @param techDev Address of technical developer
     */
    function createGroup(
        uint256 groupId,
        address[] memory payees,
        uint256[] memory shares,
        address chatModerator,
        address techDev,
        uint256[] memory tokenCaps
    ) external onlyRole(ADMIN_ROLE) {
        require(!userGroups[groupId].exists, "Group already exists");
        require(payees.length == shares.length && payees.length > 0, "Invalid payees");
        require(tokenCaps.length == 63, "Need 63 caps");

        PaymentSplitter splitter = new PaymentSplitter(payees, shares);

        userGroups[groupId] = UserGroup({
            paymentSplitter: address(splitter),
            chatModerator: chatModerator,
            techDev: techDev,
            exists: true
        });

        emit GroupCreated(groupId, address(splitter), chatModerator, techDev);

        uint256 base = groupId * 64;
        for (uint256 i = 0; i < 63; i++) {
            _maxSupply[base + i + 1] = tokenCaps[i];
        }
    }

    /**
     * @dev Get information about a user group.
     */
    function getGroup(uint256 groupId) external view returns (UserGroup memory) {
        require(userGroups[groupId].exists, "Group not found");
        return userGroups[groupId];
    }

    /**
     * @dev Mint tokens associated with a group. Only admins may mint.
     * @param to Recipient address
     * @param id Token id
     * @param amount Amount to mint
     * @param data Data passed to ERC1155
     */
    function mint(
        address to,
        uint256 id,
        uint256 amount,
        bytes memory data
    ) external onlyRole(ADMIN_ROLE) {
        uint256 gid = groupIdForToken(id);
        require(userGroups[gid].exists, "Group not set for token");
        uint256 cap = _maxSupply[id];
        if (cap > 0) {
            require(_minted[id] + amount <= cap, "Exceeds cap");
            _minted[id] += amount;
        }
        _mint(to, id, amount, data);
    }

    /// @inheritdoc ERC1155
    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC1155, AccessControl)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}

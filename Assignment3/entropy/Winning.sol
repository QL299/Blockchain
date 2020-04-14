pragma solidity ^0.6.4;

contract EtheremonLite {
    function initMonster(string memory _monsterName) public {}
    function getName(address _monsterAddress) public view returns(string memory) {}
    function getNumWins(address _monsterAddress) public view returns(uint) {}
    function getNumLosses(address _monsterAddress) public view returns(uint) {}
    function battle() public returns(uint256){}
}

contract WinBattle {

    // Placeholder; TODO for Q2 
	EtheremonLite el;
    constructor() public {
        el = EtheremonLite(address(0x9E30144D5e89e7718339D12f526705A85BEDD8F3));
        el.initMonster("ql299");
    }

    function winning() public {
        uint dice = uint(blockhash(block.number - 1));
        dice = dice / 85;
        if (dice % 3 == 0) {
    	    el.battle();
        }
    }
    
    function getElName(address monsterAddr) public view returns(string memory){
        return el.getName(monsterAddr);
    }
    
    function getElWin(address monsterAddr) public view returns(uint){
        return el.getNumWins(monsterAddr);
    }
    
    function getElLoss(address monsterAddr) public view returns(uint) {
        return el.getNumLosses(monsterAddr);
    }  
}



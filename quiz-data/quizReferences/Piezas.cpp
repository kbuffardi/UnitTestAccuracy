#include "Piezas.h"
#include <vector>
/** CLASS Piezas
 * Class for representing a Piezas vertical board, which is roughly based
 * on the game "Connect Four" where pieces are placed in a column and 
 * fall to the bottom of the column, or on top of other pieces already in
 * that column. For an illustration of the board, see:
 *  https://en.wikipedia.org/wiki/Connect_Four
 *
 * Board coordinates [row,col] should match with:
 * [2,0][2,1][2,2][2,3]
 * [1,0][1,1][1,2][1,3]
 * [0,0][0,1][0,2][0,3]
 * So that a piece dropped in column 2 should take [0,2] and the next one
 * dropped in column 2 should take [1,2].
**/


/**
 * Constructor sets an empty board (default 6 rows, 7 columns) and 
 * specifies it is X's turn first
**/
Piezas::Piezas()
{
	board.resize(BOARD_ROWS);
	for(int r=0; r<BOARD_ROWS; r++)
		board[r].resize(BOARD_COLS);
	reset();
}

/**
 * Resets each board location to the Blank Piece value, with a board of the
 * same size as previously specified (or default if overloaded constructor
 * is never called).
**/
void Piezas::reset()
{
	for(int r=0; r<BOARD_ROWS; r++)
		for(int c=0; c<BOARD_COLS; c++)
			board[r][c]=Blank;
	turn = X;
}

/**
 * Places a piece of the current turn on the board, returns what
 * piece is placed, and toggles which Piece's turn it is. dropPiece does 
 * NOT allow to place a piece in a location where a column is full.
 * In that case, dropPiece returns Piece Blank value 
 * Out of bounds coordinates return the Piece Invalid value
 * Trying to drop a piece where it cannot be placed loses the player's turn
**/ 
Piece Piezas::dropPiece(int column)
{
	Piece status = Blank;
	if( column >= 0 && column < BOARD_COLS )
	{
		for(int r=0; r<BOARD_ROWS; r++)
		{
			if( board[r][column] == Blank )
			{
				board[r][column] = turn;
				status = turn;
				break;
			}
			else if( r == BOARD_ROWS-1 ) //column is full
			{
				status = Blank;
			}
		}
	}
	else
		status = Invalid;

	if( turn == X )
		turn = O;
	else
		turn = X;
	return status;
}

/**
 * Returns what piece is at the provided coordinates, or Blank if there
 * are no pieces there, or Invalid if the coordinates are out of bounds
**/
Piece Piezas::pieceAt(int row, int column)
{
	if( row >= 0 && row < BOARD_ROWS
		&& column >= 0 && column < BOARD_COLS )
	{
		return board[row][column];
	}
	else
	{
		return Invalid;
	}
}

/**
 * Returns which Piece has won, if there is a winner, Invalid if the game
 * is not over, or Blank if the board is filled and no one has won ("tie").
 * For a game to be over, all locations on the board must be filled with X's 
 * and O's (i.e. no remaining Blank spaces). The winner is which player has
 * the most adjacent pieces in a single line. Lines can go either vertically
 * or horizontally. If both X's and O's have the same max number of pieces in a
 * line, it is a tie.
**/
Piece Piezas::gameState()
{
	Piece winning = Invalid;
	int most=0;
	Piece current = Blank;
	int adjacent=0;

	//horizontal
	for(int r=0; r<BOARD_ROWS; r++)
	{
		adjacent = 0;
		for(int c=0; c<BOARD_COLS; c++)
		{
			if( board[r][c] == Blank ) //incomplete board
				return Invalid;
			else if( board[r][c] == X || board[r][c] == O )
			{
				if( board[r][c] == current )
				{
					adjacent++;
				}
				else
				{
					adjacent=1;
					current = board[r][c];
				}

				if( adjacent > most )
				{
					most = adjacent;
					winning = board[r][c];
				}
				else if( adjacent == most && current != winning ) //currently a tie
				{
					winning = Blank;
				}
			}
		}
	}
	
	//vertical
	current = Blank;
	for(int c=0; c<BOARD_COLS; c++)
	{
		adjacent = 0;
		for(int r=0; r<BOARD_ROWS; r++)
		{
			if( board[r][c] == Blank ) //incomplete board
				return Invalid;
			else if( board[r][c] == X || board[r][c] == O )
			{
				if( board[r][c] == current )
				{
					adjacent++;
				}
				else
				{
					adjacent=1;
					current = board[r][c];
				}

				if( adjacent > most )
				{
					most = adjacent;
					winning = board[r][c];
				}
				else if( adjacent == most && current != winning ) //currently a tie
				{
					winning = Blank;
				}
			}
		}
	}
	return winning;
}
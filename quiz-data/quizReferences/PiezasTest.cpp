/**
 * Unit Tests for Piezas
**/

#include <gtest/gtest.h>
#include "Piezas.h"
 
class PiezasTest : public ::testing::Test
{
	protected:
		PiezasTest(){} //constructor runs before each test
		virtual ~PiezasTest(){} //destructor cleans up after tests
		virtual void SetUp(){} //sets up before each test (after constructor)
		virtual void TearDown(){} //clean up after each test, (before destructor) 
};

TEST(PiezasTest, dropFirst)
{
	Piezas game;
	Piece result;
	result = game.dropPiece(0);
	ASSERT_EQ(result, X);
}

TEST(PiezasTest, dropTwo)
{
  Piezas game;
  Piece result;
  game.dropPiece(0);
  result = game.dropPiece(1);
  ASSERT_EQ(result, O);
}

TEST(PiezasTest, dropThree)
{
  Piezas game;
  Piece result;
  game.dropPiece(0);
  game.dropPiece(1);
  result = game.dropPiece(1);
  ASSERT_EQ(result, X);
}

TEST(PiezasTest, dropFull)
{
  Piezas game;
  Piece result;
  game.dropPiece(1); //X
  game.dropPiece(1); //O
  game.dropPiece(1); //X
  result = game.dropPiece(1); //full so still X
  EXPECT_EQ(game.pieceAt(0,1),X);
  EXPECT_EQ(game.pieceAt(1,1),O);
  EXPECT_EQ(game.pieceAt(2,1),X);
  ASSERT_EQ(result, Blank);
}

TEST(PiezasTest, dropUnder)
{
  Piezas game;
  Piece result;
  EXPECT_NO_THROW(result = game.dropPiece(-1));
  ASSERT_EQ(result, Invalid);
}

TEST(PiezasTest, dropOver)
{
  Piezas game;
  Piece result;
  result = game.dropPiece(4);
  ASSERT_EQ(result, Invalid);
}

TEST(PiezasTest, pieceAtUnderRow)
{
  Piezas game;
  Piece result;
  EXPECT_NO_THROW(result = game.pieceAt(-1,0));
  ASSERT_EQ(result, Invalid);
}

TEST(PiezasTest, pieceAtUnderColumn)
{
  Piezas game;
  Piece result;
  EXPECT_NO_THROW(result = game.pieceAt(0,-1));
  ASSERT_EQ(result, Invalid);
}

TEST(PiezasTest, pieceAtOverRow)
{
  Piezas game;
  Piece result;
  EXPECT_NO_THROW(result = game.pieceAt(BOARD_ROWS,0));
  ASSERT_EQ(result, Invalid);
}

TEST(PiezasTest, pieceAtOverColumn)
{
  Piezas game;
  Piece result;
  EXPECT_NO_THROW(result = game.pieceAt(0,BOARD_COLS));
  ASSERT_EQ(result, Invalid);
}

TEST(PiezasTest, pieceAtOverBoth)
{
  Piezas game;
  Piece result;
  EXPECT_NO_THROW(result = game.pieceAt(BOARD_ROWS,BOARD_COLS));
  ASSERT_EQ(result, Invalid);
}

TEST(PiezasTest, pieceAtUnderBoth)
{
  Piezas game;
  Piece result;
  EXPECT_NO_THROW(result = game.pieceAt(-1,-1));
  ASSERT_EQ(result, Invalid);
}

TEST(PiezasTest, gameStateEmpty)
{
  Piezas game;
  Piece result;
  result = game.gameState();
  ASSERT_EQ(result, Invalid);
}

TEST(PiezasTest, gameStateIncompleteColumnFull)
{
  Piezas game;
  Piece result;
  game.dropPiece(3);
  game.dropPiece(3);
  game.dropPiece(3);
  result = game.gameState();
  ASSERT_EQ(result, Invalid);
}

TEST(PiezasTest, gameStateIncompleteRowFull)
{
  Piezas game;
  Piece result;
  game.dropPiece(0);
  game.dropPiece(1);
  game.dropPiece(2);
  game.dropPiece(3);
  result = game.gameState();
  ASSERT_EQ(result, Invalid);
}

TEST(PiezasTest, gameStateIncompleteButEnoughMoves)
{
  Piezas game;
  Piece result;
  game.dropPiece(0);
  game.dropPiece(1);
  game.dropPiece(2);
  game.dropPiece(3);
  game.dropPiece(0);
  game.dropPiece(1);
  game.dropPiece(2);
  game.dropPiece(3);
  game.dropPiece(0);
  game.dropPiece(1);
  game.dropPiece(2);
  game.dropPiece(0); //can't place again, leaves one spot empty
  result = game.gameState();
  ASSERT_EQ(result, Invalid);
}

/*
 * [X][X][X][O]
 * [O][X][O][O]
 * [X][O][O][X]
*/
TEST(PiezasTest, gameStateXWinsHorizontal)
{
  Piezas game;
  Piece result;
  game.dropPiece(0); //X
  game.dropPiece(0); //O
  game.dropPiece(0); //X
  game.dropPiece(1); //O
  game.dropPiece(1); //X
  game.dropPiece(2); //O
  game.dropPiece(3); //X
  game.dropPiece(2); //O
  game.dropPiece(1); //X
  game.dropPiece(3); //O
  game.dropPiece(2); //X
  game.dropPiece(3); //O
  result = game.gameState();
  ASSERT_EQ(result, X);
}

/*
 * [X][X][O][X]
 * [O][O][O][O]
 * [X][O][X][X]
*/
TEST(PiezasTest, gameStateOWinsHorizontal)
{
  Piezas game;
  Piece result;
  game.dropPiece(0); //X
  game.dropPiece(0); //O
  game.dropPiece(0); //X
  game.dropPiece(1); //O
  game.dropPiece(3); //X
  game.dropPiece(1); //O
  game.dropPiece(2); //X
  game.dropPiece(2); //O
  game.dropPiece(1); //X
  game.dropPiece(3); //O
  game.dropPiece(3); //X
  game.dropPiece(2); //O
  result = game.gameState();
  ASSERT_EQ(result, O);
}

/*
 * [O][X][O][X]
 * [X][O][O][O]
 * [X][O][X][X]
*/
TEST(PiezasTest, gameStateOWinsHorizontalLastThree)
{
  Piezas game;
  Piece result;
  game.dropPiece(0); //X
  game.dropPiece(1); //O
  game.dropPiece(3); //X
  game.dropPiece(1); //O
  game.dropPiece(0); //X
  game.dropPiece(3); //O
  game.dropPiece(2); //X
  game.dropPiece(2); //O
  game.dropPiece(3); //X
  game.dropPiece(2); //O
  game.dropPiece(1); //X
  game.dropPiece(0); //O
  result = game.gameState();
  ASSERT_EQ(result, O);
}

/*
 * [O][O][X][X]
 * [O][X][O][X]
 * [X][O][O][X]
*/
TEST(PiezasTest, gameStateXWinsVertical)
{
  Piezas game;
  Piece result;
  game.dropPiece(3);
  game.dropPiece(2);
  game.dropPiece(3);
  game.dropPiece(2);
  game.dropPiece(3);
  game.dropPiece(1);
  game.dropPiece(0);
  game.dropPiece(0);
  game.dropPiece(1);
  game.dropPiece(0);
  game.dropPiece(2);
  game.dropPiece(1);
  result = game.gameState();
  ASSERT_EQ(result, X);
}

/*
 * [O][O][X][O]
 * [X][O][O][X]
 * [X][O][X][X]
*/
TEST(PiezasTest, gameStateOWinsVertical)
{
  Piezas game;
  Piece result;
  game.dropPiece(2);
  game.dropPiece(1);
  game.dropPiece(3);
  game.dropPiece(1);
  game.dropPiece(0);
  game.dropPiece(2);
  game.dropPiece(0);
  game.dropPiece(0);
  game.dropPiece(3);
  game.dropPiece(1);
  game.dropPiece(2);
  game.dropPiece(3);
  result = game.gameState();
  ASSERT_EQ(result, O);
}

/*
 * [X][X][O][O]
 * [X][X][O][O]
 * [X][X][O][O]
*/
TEST(PiezasTest, gameStateTie)
{
  Piezas game;
  Piece result;
  game.dropPiece(0);
  game.dropPiece(3);
  game.dropPiece(0);
  game.dropPiece(3);
  game.dropPiece(0);
  game.dropPiece(3);
  game.dropPiece(1);
  game.dropPiece(2);
  game.dropPiece(1);
  game.dropPiece(2);
  game.dropPiece(1);
  game.dropPiece(2);
  result = game.gameState();
  ASSERT_EQ(result, Blank);
}

/*
 * [X][O][X][O]
 * [X][O][O][O]
 * [X][X][X][O]
*/
TEST(PiezasTest, gameStateTieThreeHorizontal)
{
  Piezas game;
  Piece result;
  game.dropPiece(0);
  game.dropPiece(3);
  game.dropPiece(0);
  game.dropPiece(3);
  game.dropPiece(0);
  game.dropPiece(3);
  game.dropPiece(1);
  game.dropPiece(1);
  game.dropPiece(2);
  game.dropPiece(2);
  game.dropPiece(2);
  game.dropPiece(1);
  result = game.gameState();
  ASSERT_EQ(result, Blank);
}
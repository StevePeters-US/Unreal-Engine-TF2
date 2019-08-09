// Copyright 1998-2019 Epic Games, Inc. All Rights Reserved.

#include "UE4_TF2GameMode.h"
#include "UE4_TF2HUD.h"
#include "UE4_TF2Character.h"
#include "UObject/ConstructorHelpers.h"

AUE4_TF2GameMode::AUE4_TF2GameMode()
	: Super()
{
	// set default pawn class to our Blueprinted character
	static ConstructorHelpers::FClassFinder<APawn> PlayerPawnClassFinder(TEXT("/Game/FirstPersonCPP/Blueprints/FirstPersonCharacter"));
	DefaultPawnClass = PlayerPawnClassFinder.Class;

	// use our custom HUD class
	HUDClass = AUE4_TF2HUD::StaticClass();
}

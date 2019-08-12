// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Runtime/Engine/Classes/Components/SceneCaptureComponent2D.h"
#include "Runtime/Engine/Classes/Engine/TextureRenderTarget2D.h"
#include "RenderTextureReader.generated.h"

UCLASS()
class UE4_TF2_API ARenderTextureReader : public AActor
{
	GENERATED_BODY()

	UPROPERTY(Category = HeightMap, EditAnywhere)
	UTextureRenderTarget2D* RenderTarget;

	UFUNCTION(BlueprintCallable, Category = "HeightMap|Update")
		void UpdateBuffer();

	UFUNCTION(BlueprintCallable, Category = "HeightMap|Texture Helper")
		FColor GetRenderTargetValue(float x, float y);
	
public:	
	// Sets default values for this actor's properties
	ARenderTextureReader();

	//USceneCaptureComponent2D *Camera;
	//UTexture2D *Texture2D;

protected:
	// Called when the game starts or when spawned
	virtual void BeginPlay() override;

public:	
	// Called every frame
	virtual void Tick(float DeltaTime) override;

private:

	TArray<FColor> ColorBuffer;

};

// Fill out your copyright notice in the Description page of Project Settings.


#include "RenderTextureReader.h"
#include "TextureResource.h"
#include "Runtime/Engine/Classes/Components/SphereComponent.h"
#include "Runtime/CoreUObject/Public/UObject/UObjectGlobals.h"
#include "Runtime/CoreUObject/Public/UObject/ConstructorHelpers.h"


// Sets default values
ARenderTextureReader::ARenderTextureReader()
{
 	// Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = true;

	/*
	RootComponent = CreateDefaultSubobject<USphereComponent>(TEXT("Root"));
	Camera = CreateDefaultSubobject<USceneCaptureComponent2D>(TEXT("Camera"));
	ConstructorHelpers::FObjectFinder<UTextureRenderTarget2D> RenderTargetAsset(TEXT("/Game/MyLittleRenderTarget"));
	//here you need to have prepared MyLittleRenderTarget asset, type RenderTarget2D. You can have one for many actors, it is duplicated.
	What is not resolved by me: i don't know if it is stable solution or it will make crash after many calls

	RenderTarget = DuplicateObject(RenderTargetAsset.Object, NULL);
	RenderTarget->InitAutoFormat(1024, 1024);
	Camera->TextureTarget = RenderTarget;*/
}

// Called when the game starts or when spawned
void ARenderTextureReader::BeginPlay()
{
	Super::BeginPlay();
	/*
	Camera->TextureTarget = RenderTarget;

	int X = RenderTarget->GetSurfaceHeight();
	int Y = RenderTarget->GetSurfaceWidth();
	GLog->Logf(TEXT("Size: %d %d"), X, Y);
	Texture2D = RenderTarget->ConstructTexture2D(this, FString("Tex2D"), EObjectFlags::RF_NoFlags);
	//FTextureRenderTargetResource *Resource = RenderTarget->GetRenderTargetResource();
	int xx = Texture2D->GetSizeX();
	int yy = Texture2D->GetSizeY();
	GLog->Logf(TEXT("Texture size: %d %d"), xx, yy);

	FTexturePlatformData *Data = Texture2D->PlatformData;
	EPixelFormat Format = Data->PixelFormat;
	GLog->Logf(TEXT("Pixel format: %d"), (uint8)(Format));
	//format of pixel is PFloatRGBA

	int size = Data->Mips[0].BulkData.GetElementSize();
	int N = Data->Mips[0].BulkData.GetElementCount();
	GLog->Logf(TEXT("Number of elements: %d, size of one element: %d"), N, size);
	//i've got 1 byte size of element

	const void *Table = Data->Mips[0].BulkData.LockReadOnly();
	Data->Mips[0].BulkData.Unlock();

	const uint16 *Tab2 = StaticCast<const uint16*>(Table);
	//ok, quick calculation. I get 8*1024*1024 bytes from 1024*1024 pixels, so one pixel got 8 bytes of data. Format is RGBA, so you can figure it yourself :)
	for (int i = 0; i < xx; i++)
		for (int j = 0; j < yy; j++) {
			int k = 4 * (i*yy + j);
			int R = Tab2[k];
			int G = Tab2[k + 1];
			int B = Tab2[k + 2];
			int A = Tab2[k + 3];
		}*/
}

// Called every frame
void ARenderTextureReader::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

}

void ARenderTextureReader::UpdateBuffer()
{
	ColorBuffer.Reset();

	if (RenderTarget != NULL)
	{

		FTextureRenderTarget2DResource* textureResource = (FTextureRenderTarget2DResource*)RenderTarget->Resource;
		if (textureResource->ReadPixels(ColorBuffer))
		{

		}
	}
}


FColor ARenderTextureReader::GetRenderTargetValue(float x, float y)
{
	float size = 10000;

	if (RenderTarget == NULL || ColorBuffer.Num() == 0)
		return FColor(0);

	float width = RenderTarget->GetSurfaceWidth();
	float height = RenderTarget->GetSurfaceHeight();

	//Conver coordinates to texture space
	float normalizedX = (x / size) + 0.5f;
	float normalizedY = (y / size) + 0.5f;

	int i = (int)(normalizedX * width);
	int j = (int)(normalizedY * height);

	if (i < 0) i = 0;
	if (i >= width) i = width - 1;
	if (j < 0) j = 0;
	if (j >= height) j = height - 1;

	int index = i + j * width;
	if (index < 0) index = 0;
	if (index >= ColorBuffer.Num()) index = ColorBuffer.Num();

	return ColorBuffer[index];
}


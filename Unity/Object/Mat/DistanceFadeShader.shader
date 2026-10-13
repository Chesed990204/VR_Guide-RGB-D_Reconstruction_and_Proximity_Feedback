// Upgrade NOTE: replaced '_Object2World' with 'unity_ObjectToWorld'

Shader "Custom/DistanceFadeShader"
{
    Properties
    {
        _MainTex("Texture", 2D) = "white" {}
    }
    SubShader
    {
        Tags { "RenderType" = "Transparent" "Queue" = "Transparent" }
        LOD 100


        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"

            struct appdata
            {
                float4 vertex : POSITION;
                float2 uv : TEXCOORD0;
                float4 color : COLOR;
            };

            struct v2f
            {
                float2 uv : TEXCOORD0;

                float4 vertex : SV_POSITION;
                float4 color : COLOR;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;

            float distanceToPlayer;
            float normalizedDistance;

            float4 vertexWorldCoord;

            float maxDistance;
            float minDistance;

            v2f vert(appdata v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = TRANSFORM_TEX(v.uv, _MainTex);

                maxDistance = 2.0f;
                minDistance = 0.0f;

                // 플레이어(카메라)와의 거리를 계산
                distanceToPlayer = length(_WorldSpaceCameraPos - mul(unity_ObjectToWorld,v.vertex).xyz);


                if (distanceToPlayer > maxDistance) {
                    normalizedDistance = 1.0f;
                }
                else {
                    normalizedDistance = (distanceToPlayer - minDistance) / (maxDistance - minDistance);
                }

                // min ~ max를 0~1로 정규화
                o.color = float4(1, normalizedDistance, normalizedDistance, 1);
                return o;
            }

            fixed4 frag(v2f i) : SV_Target
            {

                return i.color;
            }
            ENDCG
        }

    }
}

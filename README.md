# deploy-pipeline

```bash
.
├── .github
│   └── workflows
│       ├── bentoml.yml
│       └── train-for-deploy.yml
├── README.md
├── bento
│   ├── bento_packer.py
│   ├── bento_service.py
│   └── bentoml_configuration.yml
└── kutomize
    ├── base
    │   ├── deployment.yaml
    │   ├── kustomization.yaml
    │   ├── service.yaml
    │   └── training-job.yaml
    └── overlays
        └── dev
            ├── kustomization.yaml
            └── training-job-patch.json
```

- `bento_service.py` <br/>
    BentoML를 사용하여 [mnist-model](https://github.com/KIMnJANG/mnist-model)의 API 서비스를 정의합니다. 
   
- `bento_packer.py` <br/>
    BentoML를 통해 생성된 API 서비스에 [mnist-model](https://github.com/KIMnJANG/mnist-model)을 주입하고 서버에 서빙을 할 수 있도록 패킹합니다.
    
- `bentoml_configuration.yml` <br/>
   BentoML 서버의 설정을 정의합니다.

- `/kutomize/base/*`
   Kustomize를 사용하여 K8s 리소스들을 정의합니다.

- `/kutomize/overlays/dev/*`
   base에 정의된 리소스에서 실제로 dev 서버에 배포하기 위한 설정들을 overlay합니다.
   ArgoCD에서는 이 설정을 모니터링하며 지속적으로 배포합니다.

- `.github/workflows/train-for-deploy.yml` <br/>
    최적화된 하이퍼파라미트를 전달받아 배포를 위한 모델을 학습합니다.
    학습 끝나면 bentoml workflow에 모델명과 모델 버전을 포함한 Dispatch 이벤트를 전달합니다. 
    
- `.github/workflows/bentoml.yml` <br/>
    모델명과 모델 버전을 전달받아 BentoML로 패킹하고 Docker 이미지를 빌드하여 Github Packages에 배포합니다. 이미지가 성공적으로 배포되면 ArgoCD에서 바라보고있는 모델 정보를 업데이트하고 이후 ArgoCD를 통해 새 API 서비스가 배포됩니다.

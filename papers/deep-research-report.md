# 近期结构熵与结构信息理论论文全景研究

## 范围与判定标准

这份综述把“结构熵 / 结构信息理论”界定为：以 **encoding tree / partition tree / structural entropy / structural information principles** 为核心对象，而不是只在实验里顺手用一次某种“entropy”指标的论文。我把时间范围放在 **2024 年至 2026-05-19**，并优先采用 **IJCAI 2025 survey、DBLP、arXiv、AAAI、JMLR、ACM、IEEE Computer、Elsevier** 这些一手或准一手来源；对明显存在 conference→journal / preprint→conference 的条目，我会一并标出，避免你在 `refs.bib` 里重复收录。IJCAI 2025 的 survey 已经把该方向整理成“理论基础、计算方法、图学习、强化学习、跨领域应用”五大块，并明确点名了 2024–2025 年的一大批代表作，是这次检索非常好的锚点。citeturn34view0turn35view1turn17view0turn25view1

就研究脉络看，**2024 年** 的重心仍然是图上的结构学习、社交网络与事件检测、动态图与强化学习；**2025 年** 开始明显扩散到文本分类、概率表征、样本选择、图 OOD、推荐与时间序列；**2026 年到目前为止**，又进一步推进到 LLM hallucination / faithfulness、open-world 事件演化、公平 GNN、few-shot 节点分类，以及更连续化、超曲化的层次聚类。这个扩张趋势既能从 survey 的 taxonomy 中看到，也能从 2025–2026 的新论文标题和发表去向中直接验证。citeturn34view0turn29search6turn30search4turn30search0turn14search0turn15search2turn31search14turn6search2

## 你的 refs.bib 覆盖情况

你当前列出的 13 条里，**核心主干已经覆盖得不差**。我能直接或间接核验到的包括：`su2025ijcai`（IJCAI 2025 survey）、`zeng2025sidmJMLR`（JMLR 2025）、`su2025emergencecollab`（SDM 2025）、`xian2025communitySEGame`（WWW 2025）、`zeng2024scalableSSSE` 对应的半监督聚类线、`zhang2025dese`（DeSE）、`xie2025superpixel`（SIT-HSS）等。citeturn25view1turn29search6turn36search6turn5search0turn27view0turn27view2

此外，你给出的若干 2025 条目——例如 **HyperSED、SI2AF、MASGCN、SECodec、SEVC、EDEN**——在我这次快速核查里，主要是通过 **IJCAI 2025 survey 的 taxonomy 或参考文献页** 间接确认到它们确实属于这个方向；它们大多应保留在你的库里，但如果你接下来要补齐 BibTeX 元数据，我建议再单独跑一遍官方页面核 DOI、页码和最终 venue 信息。citeturn34view0turn35view1

真正的缺口主要不在你已经收的 2025 主线，而在 **2024 的方法铺垫**，以及 **2025 下半年到 2026 上半年** 迅速长出来的 NLP / LLM / fairness / recommendation / time-series / offline RL 等外延论文。换句话说，你现在的库更像“主线已在、支线偏少”。citeturn34view0turn17view0turn33view0

## 高置信新增条目

下面这批条目，我认为是**最值得优先补进** `refs.bib` 的高置信新增文献。为了降低去重风险，我把明显重复的 preprint / conference / journal 版本尽量按“论文谱系”表述。

| 建议 key | 论文 | 状态 | 为什么值得补 |
|---|---|---|---|
| `yang2024incre2dse` | *Incremental measurement of structural entropy for dynamic graphs* | Artificial Intelligence, 2024 | 这是 **动态图结构熵** 的核心理论/算法扩展，解决 encoding tree 的增量更新与 SE 的动态计算。 citeturn8search2turn17view0 |
| `cao2024mrse` | *Multi-Relational Structural Entropy* | UAI / PMLR 2024 | 把 SE 从单关系图推广到 **多关系图**，是“extension work”里非常关键的一条。 citeturn22search1turn23search11turn23search12 |
| `peng2024undbot` | *Unsupervised Social Bot Detection via Structural Information Theory* | ACM TOIS 2024 | 结构信息理论在社交机器人检测上的代表作，解释性强，而且 survey 明确把它放在 social networks 应用分支。 citeturn21search1turn20view0turn34view0 |
| `yang2024sebot` | *SeBot: Structural Entropy Guided Multi-View Contrastive Learning for Social Bot Detection* | KDD 2024 | 与 UnDBot 互补：前者偏无监督/可解释，SeBot 偏多视角对比学习与鲁棒检测。 citeturn21search0turn21search4turn33view3 |
| `yang2024adpsemevent` | *Adaptive Differentially Private Structural Entropy Minimization for Unsupervised Social Event Detection* | CIKM 2024 | 把 **差分隐私** 与 SE 最小化结合到无监督事件检测里，是你当前库里事件检测线的一个重要缺块。 citeturn21search2turn18view2 |
| `zou2024hierrecGAD` | *A Structural Information Guided Hierarchical Reconstruction for Graph Anomaly Detection* | CIKM 2024 | 标题里不显式写 SE，但结构信息引导的层次重构就是核心方法；它补齐了 **graph anomaly detection** 支线。 citeturn32search0turn32search5turn33view0 |
| `duan2024segslnc` | *Structural Entropy Based Graph Structure Learning for Node Classification* | AAAI 2024 | survey 明确把它放在 graph learning / structure augmentation 分支；这是 **SE-GSL** 在节点分类上的关键条目。 citeturn6search1turn22search5turn34view0 |
| `huang2024sec` | *SEC: More Accurate Clustering Algorithm via Structural Entropy* | AAAI 2024 | 偏聚类算法本体，和你库里半监督聚类、DeSE 形成前后衔接。 citeturn6search3turn6search11 |
| `ren2024hipart` | *Hi-PART: Going Beyond Graph Pooling with Hierarchical Partition Tree for Graph-Level Representation Learning* | ACM TKDD 2024 | 标题不含 structural entropy，但官方页面和 survey 都明确说明其核心是 **用 structure entropy 构建 hierarchical partition tree**。 citeturn36search0turn36search15turn34view0 |
| `sun2024lsenet` | *LSEnet: Lorentz Structural Entropy Neural Network for Deep Graph Clustering* | ICML 2024 | 这是 **连续化 / 可微化 / 双曲化** SE 路线的起点之一，后面 IsoSEL 和 HypCSE 都能看作其后续展开。 citeturn22search2turn23search20turn23search14 |
| `xie2025ses` | *Structural-Entropy-Based Sample Selection for Efficient and Effective Learning* | ICLR 2025 | 把 SE 从图挖掘扩展到 **data selection / sample selection**，说明该方向已经进入“训练数据治理”层。 citeturn7search0turn8search4 |
| `hou2025sego` | *Structural Entropy Guided Unsupervised Graph Out-Of-Distribution Detection* | AAAI 2025 | 图 OOD 是近两年的热点，这篇基本是“SE + graph OOD”的代表作。 citeturn5search8turn24view0 |
| `liu2025sihtc` | *Hierarchical Text Classification Optimization via Structural Entropy and Singular Smoothing* | IEEE TKDE 2025 | 把 SE 实打实推进到 **hierarchical text classification**，而且还是期刊论文，不是只有 arXiv。 citeturn16search0turn18view0 |
| `huang2025sepc` | *Structural Entropy Guided Probabilistic Coding* | AAAI 2025 | survey 已把它归到 extension work；它的重要性在于把 SE 做成 **概率表征 / probabilistic encoding tree**。 citeturn36search3turn36search7turn34view0 |
| `zeng2025sihd` | *Structural Information-based Hierarchical Diffusion for Offline Reinforcement Learning* | NeurIPS 2025 / arXiv | 这是 RL 支线里非常值得补的一篇：它把结构信息原则带到 **offline RL + hierarchical diffusion**。 citeturn26search0turn26search2turn33view1 |
| `zhao2025sese` | *SeSE: A Structural Information-Guided Uncertainty Quantification Framework for Hallucination Detection in LLMs* | arXiv 2025 | 这篇标志着结构信息理论进入 **LLM 不确定性量化 / hallucination detection**。 citeturn30search4turn33view0 |
| `ye2026fairgse` | *FairGSE: Fairness-Aware Graph Neural Network without High False Positive Rates* | AAAI 2026 | 通过最大化二维 SE 处理 fairness–FPR trade-off，是 **fairness-aware GNN** 的新切口。 citeturn15search2turn15search10turn10search7 |
| `yang2026seinevent` | *Structural Entropy Guided Incremental Learning for Open-World Multimodal Social Event Detection* | AAAI 2026 | 这是 ADP-SEMEvent / HISEvent / HyperSED 之后，事件检测线里最新且很强的一篇。 citeturn19view0turn15search7turn30search5 |
| `liu2026ragsede` | *Effective and Unsupervised Social Event Detection and Evolution via RAG and Structural Entropy* | WWW 2026 | 说明这个方向已经把 **RAG、事件知识库、结构熵演化建模** 接起来了。 citeturn14search0turn14search2turn14search7 |
| `chen2026semeta` | *Structural Entropy Guided Meta-Learning for Few-Shot Node Classification* | IEEE TKDE 2026 | few-shot 节点分类方向里，SE 已经不是附属 regularizer，而是 meta-knowledge 建模核心。 citeturn9search0turn16search3turn31search14 |
| `zeng2026hypcse` | *Hyperbolic Continuous Structural Entropy for Hierarchical Clustering* | AAAI 2026 | 这是 LSEnet / IsoSEL 之后最重要的 **连续层次聚类** 路线成果之一。 citeturn6search2turn30search1turn30search9 |

除了上表，高置信但更偏“应用外延”的新增条目还有一组，也值得你补库：**MultiSPANS**（交通预测）、**Dialogues Aspect-based Sentiment Quadruple Extraction via Structural Entropy Minimization Partitioning**（对话情感四元组抽取）、**Structural entropy based graph contrastive learning for node classification**、**Structural Entropy Guided Relation Extraction on Adaptive Graph Structure**、**Enhanced Pre-training for Recommendation via Hypergraph Structural Entropy**、**Structural Entropy-based Multivariate Time Series Forecasting**、**IsoSEL**、**SEHFS**、**LANCET**、**Breaking Degradation Coupling: A Structural Entropy Guided Decoupled Framework and Benchmark for Infrared Enhancement**，以及 **Structural Entropy Guided Hierarchical Symmetric Multi-Agent Reinforcement Learning**。这些论文共同说明：SE/结构信息理论已经从“图聚类工具”变成了一个能迁移到 **NLP、LLM、视觉、推荐、时序、MARL** 的一般性结构先验。citeturn21search7turn22search0turn37search3turn37search2turn37search5turn37search16turn9search1turn8academia11turn30search0turn30search8turn12search1

## 主题演进与技术判断

如果把近两三年的论文放在一起看，这个方向最显著的技术演进有四条。

第一条是 **从离散、启发式的 SE 最小化，走向连续、可微、双曲几何化的结构学习**。LSEnet 明确提出 differentiable structural information，并把它放进 Lorentz 模型；随后 DeSE 做到深度无监督图聚类；IsoSEL 继续把 partition tree 学习和 hyperbolic contrastive learning 结合；HypCSE 则进一步把“continuous structural entropy + hierarchical clustering”推成 2026 年 AAAI 论文。这一条主线很可能会继续主导后续 graph clustering / hierarchical clustering 方向。citeturn22search2turn5search0turn9search1turn6search2

第二条是 **从简单图走向多关系图、动态图、超图和更复杂语义图**。MrSE 是多关系扩展；动态图增量测度把 SE 推向 evolving graph setting；推荐里已经出现了 “hypergraph structural entropy”；LLM uncertainty / hallucination 里则出现了 semantic graph、directed semantic graph、claim graph 这类语义结构。也就是说，SE 的对象正在从“普通 network”迁移到“结构更复杂、语义更强、时间更动态”的图。citeturn22search1turn8search2turn37search5turn30search4

第三条是 **从 graph mining 走向 decision making 与 generation**。在 RL 里，SIDM/JMLR、SI2E、Emergence of Cooperation、SIHD 分别覆盖了 hierarchical decision making、exploration、MARL cooperation 和 offline RL diffusion；在事件检测里，结构熵又和 privacy、incremental learning、RAG、event evolution 结合。这说明结构信息原则已经不再只是“聚类/社区发现”的目标函数，而是在做 **层次抽象、技能分解、轨迹建模、长期演化表示**。citeturn29search6turn29search0turn25view1turn26search0turn21search2turn15search7turn14search0

第四条是 **进入 LLM 与现代表征学习基础设施层**。SEPC 处理 probabilistic coding，SES 处理 sample selection，SeSE 与 LANCET 处理 hallucination / faithfulness，FairGSE 处理 fairness–FPR，说明它已经不只是学术上的图论分区工具，而是在被当作一种 **结构先验、压缩先验、全局不确定性度量** 来使用。这个方向如果继续发展，最可能的下一步会是：更大规模 benchmark、统一的 differentiable implementation、以及同 spectral / modularity / map equation 的系统性比较。citeturn36search3turn7search0turn30search4turn30search0turn15search10turn34view0

## 对你的文献库最实用的补库建议

如果你的目标是把 `refs.bib` 从“有主线”提升到“可写综述 / 能撑 related work”，我建议优先按下面这个顺序补。

**先补方法根基**：`Incremental measurement of structural entropy for dynamic graphs`、`Multi-Relational Structural Entropy`、`LSEnet`、`Structural Entropy Based Graph Structure Learning for Node Classification`、`Hi-PART`。这五篇补上以后，你的“理论—算法—图学习”链条会完整很多。citeturn8search2turn22search1turn22search2turn6search1turn36search0

**再补 social / event 主线缺口**：`Unsupervised Social Bot Detection via Structural Information Theory`、`SeBot`、`Adaptive Differentially Private Structural Entropy Minimization for Unsupervised Social Event Detection`、`Structural Entropy Guided Incremental Learning for Open-World Multimodal Social Event Detection`、`Effective and Unsupervised Social Event Detection and Evolution via RAG and Structural Entropy`。这样你在社交网络与事件检测方向就不会只剩你当前那几篇“中间节点”，而会形成前后连续的谱系。citeturn21search1turn21search0turn21search2turn15search7turn14search0

**最后补跨域扩展**：`Structural-Entropy-Based Sample Selection for Efficient and Effective Learning`、`Hierarchical Text Classification Optimization via Structural Entropy and Singular Smoothing`、`Structural Information-based Hierarchical Diffusion for Offline Reinforcement Learning`、`SeSE`、`Enhanced Pre-training for Recommendation via Hypergraph Structural Entropy`、`Structural Entropy-based Multivariate Time Series Forecasting`。补完这些，你的库就会从“SE for graphs”升级成“SE as a general structural-information paradigm”。citeturn7search0turn16search0turn26search0turn30search4turn37search5turn37search16

如果你打算在 `refs.bib` 里做去重，我会特别留意三类版本关系：**SDM 2024 → TKDE 2025** 的半监督聚类线，**arXiv 2024 “Effective Reinforcement Learning…” → JMLR 2025 SIDM** 的 RL 线，以及 **arXiv 2025 HypCSE / AAAI 2026** 这样的 preprint→conference 线。前两类很容易在引用库里出现“名字不同、内容同源”的重复。citeturn27view0turn29search9turn29search6turn30search1turn30search9

## 开放问题与局限

我这次给你的不是“互联网绝对完备清单”，而是一个 **高置信、可直接用于补库和写综述的 paper map**。有三点限制需要明说。

其一，我刻意**排除了**那些只把“structural entropy”当成通用统计或物理术语、但与 encoding tree / structural information theory 主线无关的论文；否则“all recent papers”会迅速失去边界。其二，少数你已经列出的条目——尤其是 **HyperSED、SI2AF、MASGCN、SECodec、SEVC、EDEN**——我在这次时间内主要是通过 **IJCAI 2025 survey 的 taxonomy / references** 做到间接确认，没有逐篇重开官方页面核全元数据。其三，若干 2025–2026 条目仍处于 **arXiv、OnlineFirst、Journal Pre-proof** 阶段，最终页码、卷期、甚至题名小改都还有可能变化。citeturn34view0turn35view1turn37search2turn37search3turn30search0turn8academia11

整体判断是：**你的当前库已经覆盖了 2025 年主干，但明显低估了 2024 年奠基工作和 2025 下半年—2026 上半年在 LLM、fairness、RL、推荐、时序上的外延爆发。** 如果只补上文提到的高优先级条目，你的文献库就会从“可用”变成“足够支撑一篇像样的 recent advances / survey-style related work”。citeturn34view0turn33view0turn30search4turn15search2turn14search0
#include "explorer.hpp"
#include <limits>

namespace fmo {
    namespace {
        constexpr int int16_max = std::numeric_limits<int16_t>::max();
    }

    void registerExplorerV1() {
        Algorithm::registerFactory(
            "explorer-v1", [](const Algorithm::Config& config, Format format, Dims dims) {
                return std::unique_ptr<Algorithm>(new ExplorerV1(config, format, dims));
            });
    }

    ExplorerV1::~ExplorerV1() = default;

    ExplorerV1::ExplorerV1(const Config& cfg, Format format, Dims dims)
        : mDiff(cfg.diff), mCfg(cfg) {
        if (dims.width <= 0 || dims.height <= 0 || dims.width > int16_max ||
            dims.height > int16_max) {
            throw std::runtime_error("bad config");
        }

        if (dims.height <= mCfg.maxImageHeight) {
            throw std::runtime_error(
                "bad config: expecting height to be larger than maxImageHeight");
        }

        if (format != Format::GRAY && format != Format::BGR) {
            throw std::runtime_error("bad format");
        }

        // allocate the source level
        mSourceLevel.format = format;
        mSourceLevel.dims = dims;
        mSourceLevel.image1.resize(format, dims);
        mSourceLevel.image2.resize(format, dims);
        mSourceLevel.image3.resize(format, dims);
        int step = 1;

        format = mSubsampler.nextFormat(format);
        dims = mSubsampler.nextDims(dims);
        step = mSubsampler.nextPixelSize(step);

        // create as many decimation levels as required to get below maximum height
        mIgnoredLevels.reserve(4);
        while (dims.height > mCfg.maxImageHeight) {
            mIgnoredLevels.emplace_back();
            mIgnoredLevels.back().image.resize(format, dims);

            format = mSubsampler.nextFormat(format);
            dims = mSubsampler.nextDims(dims);
            step = mSubsampler.nextPixelSize(step);
        }

        // allocate the processed level
        mLevel.image1.resize(format, dims);
        mLevel.image2.resize(format, dims);
        mLevel.image3.resize(format, dims);
        mLevel.diff1.resize(Format::GRAY, dims);
        mLevel.diff2.resize(Format::GRAY, dims);
        mLevel.preprocessed.resize(Format::GRAY, dims);
        mLevel.step = step;
    }

    void ExplorerV1::setInputSwap(Image& input) {
        if (input.format() != mSourceLevel.image1.format()) {
            throw std::runtime_error("setInputSwap(): bad format");
        }
        if (input.dims() != mSourceLevel.image1.dims()) {
            throw std::runtime_error("setInputSwap(): bad dimensions");
        }

        mFrameNum++;
        createLevelPyramid(input);
        preprocess();
        findStrips();
        findComponents();
        analyzeComponents();
        findTrajectories();
        analyzeTrajectories();
        findObjects();
    }
}

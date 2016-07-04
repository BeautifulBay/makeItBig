ifeq (,$(findstring CYGWIN,$(shell uname -sm)))
ifneq (1,$(strip $(shell expr $(MAKE_VERSION) \>= 3.81)))
$(error stopping)
endif
endif

ifneq ($(filter $(dont_bother_goals), $(MAKECMDGOALS)),)
dont_bother := true
endif

# Targets that provide quick help on the build system.
include $(BUILD_SYSTEM)/help.mk

# Set up various standard variables based on configuration
# and host information.
include $(BUILD_SYSTEM)/config.mk

# CTS-specific config.
-include cts/build/config.mk

ifneq ($(VERSION_CHECK_SEQUENCE_NUMBER),$(VERSIONS_CHECKED))

$(info Checking build tools versions...)

ifneq ($(HOST_OS),windows)
# check for a case sensitive file system
ifneq xxxxxxx

endif
endif

endif


ifeq ($(strip $(java_version)),)
endif

# Check for the current JDK.
#
# For Java 1.7, we require OpenJDK on linux and Oracle JDK on Mac OS.
requires_openjdk := false
ifeq ($(HOST_OS), linux)
requires_openjdk := true
endif


ags_to_install := debug eng
include $(BUILD_SYSTEM)/post_clean.mk

ifeq ($(stash_product_vars),true)
  $(call assert-product-vars, __STASHED)
endif

include $(BUILD_SYSTEM)/legacy_prebuilts.mk
ifneq ($(filter-out $(GRANDFATHERED_ALL_PREBUILT),$(strip $(notdir $(ALL_PREBUILT)))),)
	xxxx
endif

define get-32-bit-modules
$(strip $(foreach m,$(1),\
  $(if $(ALL_MODULES.$(m)$(TARGET_2ND_ARCH_MODULE_SUFFIX).CLASS),\
    $(m)$(TARGET_2ND_ARCH_MODULE_SUFFIX))))
endef
# Get a list of corresponding 32-bit module names, if one exists;
# otherwise return the original module name
define get-32-bit-modules-if-we-can
$(strip $(foreach m,$(1),\
  $(if $(ALL_MODULES.$(m)$(TARGET_2ND_ARCH_MODULE_SUFFIX).CLASS),\
    $(m)$(TARGET_2ND_ARCH_MODULE_SUFFIX),
    $(m))))
endef
 )\
)
r_r :=

define add-required-deps
$(1): | $(2)
endef

